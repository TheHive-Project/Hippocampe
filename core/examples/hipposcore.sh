#!/usr/bin/env bash


curl -i -H "Content-Type: application/json" -X POST -d '
{
	"perugemstones.com" : {"type" : "domain"},
	"hnliyin.com" : {"type" : "domain"},
	"199.9.24.1" : {"type" : "ip"},
	"198.23.78.98" : {"type" : "ip"},
	"223.184.173.74" : {"type" : "ip"}
}' http://localhost:5000/hippocampe/api/v1.0/hipposcore


