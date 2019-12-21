#!/bin/bash

NAME="Mughal App"                                  # Name of the application
DJANGODIR=/home/lals/Desktop/Invoice_Application_Django/Invoice
          # Django project directory
SOCKFILE=/home/lals/Desktop/Invoice_Application_Django/run/gunicorn.sock  # we will communicte using this unix socket
USER=lals                                       # the user to run as
GROUP=lals                                     # the group to run as
NUM_WORKERS=1                                    # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=Invoice.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=Invoice.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /home/lals/Desktop/djgo/bin/activate
export DJANGO_SETTINGS_MODULE=/home/lals/Desktop/Invoice_Application_Django/Invoice/Invoice.settings
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /home/lals/Desktop/djgo/bin/gunicorn /home/lals/Desktop/Invoice_Application_Django/Invoice/Invoice.wsgi  --name 'Mughal'  --log-file=-
