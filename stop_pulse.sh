#!/bin/bash

systemctl --user stop pulseaudio.socket
systemctl --user stop pulseaudio.service
systemctl --user disable pulseaudio.socket
systemctl --user disable pulseaudio.service
systemctl --user mask pulseaudio.socket
systemctl --user mask pulseaudio.service

