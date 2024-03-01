un = "UNPROCESSED"
pro = "PROCESSED"
fail = "COMPLETELY_FAILED"
partial = "PARTIAL_SUCCESS"


a = partial


result = pro if a == pro or a == partial else un

print(result)