import os
import re
from pathlib import Path

own_name = os.path.splitext(os.path.basename(__file__))[0] + '.exe'


def work(path: Path):
    if not path:
        return
    split_str = input('\n请输入分割符（可以有多个）, 以 "reg:" 开头则启用正则表达式：\n')
    if split_str.startswith('reg:'):
        split_pat = re.compile(split_str.replace('reg:', ''))
    else:
        split_pat = re.compile(f'[{split_str}]')

    print('\n文件名会被如下分割：\n')
    show_limit = 3
    for child in sorted(path.iterdir()):
        if child.is_dir():
            continue
        old_name = child.name
        if old_name == own_name:
            continue
        old_name_list = re.split(split_pat, old_name)
        print(old_name_list)
        show_limit -= 1
        if not show_limit:
            break

    reorder = input(
        '\n请使用旧文件名的位置号（从 1 开始）来组成新文件名，\n'
        '可以直接填充新的部分（以<>括起待填充的内容），\n'
        '<>中的*会替换为数字递增填充，以旧文件名排序，\n'
        '<>中仍然可以以 "/位置号/" 来引入旧文件名某部分内容，\n'
        '不同部分以空格间隔开来：\n'
    )
    reorder_list = reorder.split()

    link = input(
        '\n请输入新文件名各部分连接符（后缀 "." 不受影响），直接回车取消所有连接符，\n'
        '连接符之间以|分隔，\n'
        '连接符不够时将重复最后一个连接符：\n'
    )
    link_list = link.split('|')

    count = 0
    control = ''
    for child in sorted(path.iterdir()):
        if child.is_dir():
            continue
        old_name = child.name
        if old_name == own_name:
            continue
        old_name_list = re.split(split_pat, old_name)
        new_name_list = list(reorder_list)
        for index, item in enumerate(reorder_list):
            if item.startswith('<') and item.endswith('>'):
                item = item[1:-1]
                temp = item.split('/')
                for i, t in enumerate(temp):
                    if t == '' or t == '/':
                        continue
                    elif t.isdigit():
                        num = int(t) - 1
                        if num in range(len(old_name_list)):
                            temp[i] = old_name_list[num]
                item = ''.join(temp)
                new_name_list[index] = item.replace('*', str(count))
            elif item.isdigit():
                num = int(item) - 1
                if num in range(len(old_name_list)):
                    new_name_list[index] = old_name_list[num]
        new_name = new_name_list[0]
        link_now = link_list[0]
        for i in range(1, len(new_name_list)):
            if i == len(new_name_list) - 1:
                new_name += '.' + new_name_list[i]
            else:
                new_name += ('' if new_name_list[i] ==
                             '' else link_now) + new_name_list[i]
            if i < len(link_list):
                link_now = link_list[i]
        if control == '':
            print('\n新文件名如下：\n')
            print(f'[{old_name}] --> [{new_name}]')
            control = input('\n按回车确认修改，按n回车跳过当前修改，按空格回车确认所有修改...\n')
        else:
            print(f'[{old_name}] --> [{new_name}]')
        if control.lower() == 'n':
            print('已取消')
            control = ''
            continue
        child.rename(child.with_name(new_name))
        count += 1

    input('\n修改完成，按回车可以继续修改当前文件夹下的文件...\n')
    work(path)


if __name__ == '__main__':
    dir_path = ''
    # os.path.exists(dir_path)
    while not os.path.isdir(dir_path):
        dir_path = input('请输入工作文件夹地址：\n')
    work(Path(dir_path))
