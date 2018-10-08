with open('../stickmanranger.log') as o:
    p = o.readlines()[-1]

with open('changes.html', 'r+') as o:
    d = o.readlines()
    import pprint
    pprint.pprint(d)
    index = d.index(
        '       </div> <!-- this is a comment just for automation.-->\n')
    #d.insert(index, '<br/>hiiiiiiii\n')
    d.insert(index, ''.join(('        <br>', p, '\n')))
    o.seek(0)
    o.write(''.join(d))
    o.truncate()
