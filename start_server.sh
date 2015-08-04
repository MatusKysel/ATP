#!/bin/sh

SERVER_APP='ATPServer.py'
PID_FILE='server.pid'
LOG_FILE='ATPServer.log'
SERVER_EXEC='python3' #

start_app (){
    if [ -f $PID_FILE ]
    then
        echo "$PID_FILE exists, process is already running or crashed"
        exit 1
    else
        echo "Starting server app..."
        rm -f $LOG_FILE;
        touch $LOG_FILE;
        $SERVER_EXEC $SERVER_APP &
        echo $! > $PID_FILE;
    fi
}

stop_app (){
    if [ ! -f $PID_FILE ]
    then
        echo "$PID_FILE does not exist, process is not running"
        exit 1
    else
        echo "Stopping $SERVER_APP ..."
        echo "Killing `cat $PID_FILE`"
        kill `cat $PID_FILE`;
        rm -f $PID_FILE;
        echo "Server stopped"
    fi
}

case "$1" in
    start)
        start_app
    ;;

    stop)
        stop_app
    ;;

    restart)
        stop_app
        start_app
    ;;

    status)
        if [ -f $PID_FILE ]
        then
            PID=`cat $PID_FILE`
            if [ -z "`ps ef | awk '{print $1}' | grep "^$PID$"`" ]
            then
                echo "Server app stopped but pid file exists"
            else
                echo "Server app running with pid $PID"

            fi
        else
            echo "Server app stopped"
        fi
    ;;

    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
    ;;
esac

