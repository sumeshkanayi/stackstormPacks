authToken=$(st2 auth st2admin -p Sia123|grep "token"|awk '{print $4}')

echo "export ST2_AUTH_TOKEN=$authToken"

