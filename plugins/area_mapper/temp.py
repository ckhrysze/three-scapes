import re
ansi = re.compile("^((\[((.)*?)m))\w+")
for group in ansi.search("""[33mThe cobbles give way to a weird, twisting tile that makes
    print group