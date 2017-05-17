authToken=$(st2 auth st2admin -p Just4DevOps|grep "token"|awk '{print $4}')

echo "export ST2_AUTH_TOKEN=$authToken"

