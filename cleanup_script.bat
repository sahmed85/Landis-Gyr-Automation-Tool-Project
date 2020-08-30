:: This is a test windows batch file to delete php files that are uploaded.
:: input is the session_id from the php call

cd "C:\wamp64\www\upgradeplantool\uploads\"
del *.* /q

cd "C:\wamp64\www\upgradeplantool\session_files\"
del *.* /q