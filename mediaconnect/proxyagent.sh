## Amazon Web Services, Inc. or its affiliates
## Confidential Strictly Private
##
## ---------------------------------------------------------------------------
##          COPYRIGHT NOTICE
## ---------------------------------------------------------------------------
## Copyright 2023, Amazon Web Services, Inc. or its affiliates. All rights reserved.
##
## Amazon Web Services or its affiliates owns the sole copyright to this software.
## Under international copyright laws you (1) may not make a copy of this software
## except for the purposes of maintaining a single archive copy, (2) may not
## derive works herefrom, (3) may not distribute this work to others. These
## rights are provided for information clarification, other restrictions of
## rights may apply as well.
##
## This is an unpublished work.
## ---------------------------------------------------------------------------
## WARRANTY
## ---------------------------------------------------------------------------
## Amazon Web Services, Inc. or its affiliates MAKES NO WARRANTY OF ANY KIND WITH REGARD TO THE USE OF ## THIS SOFTWARE, EITHER EXPRESSED OR IMPLIED,INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF ## MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. FOR MORE INFORMATION CONSULT THE AWS ELEMENTAL ## END USER LICENSE AGREEMENT: https://aws.amazon.com/legal/elemental-appliances-software-eula/
## ---------------------------------------------------------------------------

ADDONS=/opt/amazon/httpproxy/addons
# Delete the cert on start since it has a max of 3 years lifetime, recreated on start
rm -f /home/httpproxy/.mitmproxy/*

# If this is the proxy for the agents (not for a bridge), then enter the aws-elemental network namespace which is what
# we use for the DIND container so that the bridges continue to run even if it exits.
enter=""
if [[ -z "$ELEMENTAL_ANYWHERE_TASK_ARN" && -z "$INSTANCE_LEVEL_AGENT" ]]; then
  enter="nsenter --net=/hostnetns/aws-elemental"
  pid=$$
  duration=1003d # About 2.75 years since 3 non-leap years is 1095 days.
  (sleep $duration && kill $pid) &
fi
$enter /opt/amazon/bin/httpproxy -s $ADDONS/redirect.py -s $ADDONS/redirect-websocket.py -s $ADDONS/sigv4.py "$@"
