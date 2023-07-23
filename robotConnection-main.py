import urllib
from urllib import parse
import tornado
from tornado import httpclient
import requests

import rtde.rtde as rtde
import rtde.rtde_config as rtde_config
import rtde.csv_writer as csv_writer
import eventsource.request as request
import logging
import sys

sys.path.append("..")

if __name__ == '__main__':
    # connects with robot, sends recipe, receives data --> currently written into csv file and send to flask app
    # modified version of record.py; see copyright below:
    # !/usr/bin/env python
    # Copyright (c) 2020-2022, Universal Robots A/S,
    # All rights reserved.
    # Redistribution and use in source and binary forms, with or without
    # modification, are permitted provided that the following conditions are met:
    #    * Redistributions of source code must retain the above copyright
    #      notice, this list of conditions and the following disclaimer.
    #    * Redistributions in binary form must reproduce the above copyright
    #      notice, this list of conditions and the following disclaimer in the
    #      documentation and/or other materials provided with the distribution.
    #    * Neither the name of the Universal Robots A/S nor the names of its
    #      contributors may be used to endorse or promote products derived
    #      from this software without specific prior written permission.
    # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    # ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    # WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    # DISCLAIMED. IN NO EVENT SHALL UNIVERSAL ROBOTS A/S BE LIABLE FOR ANY
    # DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    # (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    # LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    # ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    # (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    # SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    host = '172.17.0.2'
    port = 30004
    frequency = 50
    config = 'recipe.xml'
    buffered = True
    output = 'robot_data.csv'
    binary = False
    conf = rtde_config.ConfigFile(config)
    output_names, output_types = conf.get_recipe("out")
    http_client = tornado.httpclient.AsyncHTTPClient()

    con = rtde.RTDE(host, port)
    con.connect()

    # get controller version
    con.get_controller_version()

    # setup recipes
    if not con.send_output_setup(output_names, output_types, frequency=frequency):
        logging.error("Unable to configure output")
        sys.exit()

    # start data synchronization
    if not con.send_start():
        logging.error("Unable to start synchronization")
        sys.exit()

    writeModes = "w"
    with open(output, writeModes) as csvfile:
        writer = None
        writer = csv_writer.CSVWriter(csvfile, output_names, output_types)
        writer.writeheader()

        i = 1
        keep_running = True
        while keep_running:

            if i % frequency == 0:
                sys.stdout.write("\r")
                sys.stdout.write("{:3d} samples.".format(i))
                sys.stdout.flush()
            try:
                if buffered:
                    state = con.receive_buffered(binary)
                else:
                    state = con.receive(binary)
                if state is not None:
                    writer.writerow(state)
                    i += 1
                    # put data into array to put into events and ready to push to client
                    data = []
                    for i in range(len(output_names)):
                        value = state.__dict__[output_names[i]]
                        # data ist liste von arrays: data[1] enthält die joint pos., data[2] die tcp pos.
                        # jedes array hat 6 Werte
                        data.append(value)
                    # self.notify(data)
                    # print(data)
                    data1 = " ".join(str(x) for x in data[0])
                    data2 = " ".join(str(x) for x in data[1])
                    tuples = (data1, data2)
                    datastr = " ".join(tuples)
                    print(datastr)
                    answer = requests.get(f'http://127.0.0.1:5000/event/{datastr}')
                    print(answer.status_code)

            except KeyboardInterrupt:
                keep_running = False
            except rtde.RTDEException:
                con.disconnect()
                sys.exit()

    sys.stdout.write("\rComplete!            \n")
    answer = requests.get(f'http://127.0.0.1:5000/event/{"finished"}')
    print(answer.status_code)

    con.send_pause()
    con.disconnect()
