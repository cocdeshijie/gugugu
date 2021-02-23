def file_size(bytes):
    suffixes = ['B', 'KB', 'MB', 'GB']
    i = 0
    while bytes >= 1024 and i < len(suffixes)-1:
        bytes /= 1024.
        i += 1
    f = ('%.2f' % bytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])

print(file_size(536870912))