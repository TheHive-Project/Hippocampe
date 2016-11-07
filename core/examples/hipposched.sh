#!/usr/bin/env bash


curl -i -H "Content-Type: application/json" -X POST -d '
{
	"time" : "* */12 * * *"
}' http://localhost:5000/hippocampe/api/v1.0/hipposched
