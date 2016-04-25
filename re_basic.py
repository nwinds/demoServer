import re

pattern = re.compile(r'login')
match = pattern.match(r'login?cid=xxxx&eid=xxxxx&url=xxxx')
if match:
    print(match.group())

print('re matching finished')
