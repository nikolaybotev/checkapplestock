#!/bin/sh

PRODUCT_FILE="${1}"
TO_NUMBER="${2}"
SENDSMS="${3:-/bin/echo}"

echo "Started on $(date)"
echo "- using $PRODUCT_FILE"

cd "$(dirname $0)"

A="$(./check-availability.py -f $PRODUCT_FILE)"

if [ ".$A" = "." ]; then
  echo NO AVAILABILITY
else
  echo "$A"
  echo "Notifying $TO_NUMBER using $SENDSMS ..."
  "$SENDSMS" "$TO_NUMBER" "$A"
fi

echo "Finished on $(date)"