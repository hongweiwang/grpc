# Copyright 2015, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""The Python implementation of the GRPC interoperability test client."""

import argparse
from oauth2client import client as oauth2client_client

from grpc.early_adopter import implementations

from grpc_interop import methods
from grpc_interop import resources

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def _args():
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--server_host', help='the host to which to connect', type=str)
  parser.add_argument(
      '--server_port', help='the port to which to connect', type=int)
  parser.add_argument(
      '--test_case', help='the test case to execute', type=str)
  parser.add_argument(
      '--use_tls', help='require a secure connection', dest='use_tls',
      action='store_true')
  parser.add_argument(
      '--use_test_ca', help='replace platform root CAs with ca.pem',
      action='store_true')
  parser.add_argument(
      '--server_host_override',
      help='the server host to which to claim to connect', type=str)
  parser.add_argument('--oauth_scope', help='scope for OAuth tokens', type=str)
  parser.add_argument(
      '--default_service_account',
      help='email address of the default service account', type=str)
  return parser.parse_args()

def _oauth_access_token(args):
  credentials = oauth2client_client.GoogleCredentials.get_application_default()
  scoped_credentials = credentials.create_scoped([args.oauth_scope])
  return scoped_credentials.get_access_token().access_token

def _stub(args):
  if args.oauth_scope:
    metadata_transformer = lambda x: [('Authorization', 'Bearer %s' % _oauth_access_token(args))]
  else:
    metadata_transformer = lambda x: []
  if args.use_tls:
    if args.use_test_ca:
      root_certificates = resources.test_root_certificates()
    else:
      root_certificates = resources.prod_root_certificates()

    stub = implementations.stub(
        methods.SERVICE_NAME, methods.CLIENT_METHODS, args.server_host,
        args.server_port, metadata_transformer=metadata_transformer,
        secure=True, root_certificates=root_certificates,
        server_host_override=args.server_host_override)
  else:
    stub = implementations.stub(
        methods.SERVICE_NAME, methods.CLIENT_METHODS, args.server_host,
        args.server_port, secure=False)
  return stub


def _test_case_from_arg(test_case_arg):
  for test_case in methods.TestCase:
    if test_case_arg == test_case.value:
      return test_case
  else:
    raise ValueError('No test case "%s"!' % test_case_arg)


def _test_interoperability():
  args = _args()
  stub = _stub(args)
  test_case = _test_case_from_arg(args.test_case)
  test_case.test_interoperability(stub, args)


if __name__ == '__main__':
  _test_interoperability()
