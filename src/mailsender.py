import subprocess
import sys

s1 = '本文:テスト本文\nテストテストテスト'
s2 = '件名'
user = 'matarain'
cmd1 = 'echo \"' + s1 +'\"'
cmd2 = 'mail -s \"' + s2 + '\" ' + user
cmd = cmd1 + ' | ' + cmd2 

cp = subprocess.call(cmd,shell=True ,stdout=subprocess.PIPE)
if cp != 0:
    print('command failed.', file=sys.stderr)
    sys.exit(1)

