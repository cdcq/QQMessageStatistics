import re
import sys
import time
import jieba.posseg as pseg
import yaml
from wordcloud import WordCloud


def split_content(content):
    re_msg_head = r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{1,2}:[0-9]{2}:[0-9]{2} .+?\n'
    heads = re.findall(re_msg_head, content)
    contents = re.split(re_msg_head, content)[1:]

    assert len(heads) == len(contents)

    msg_cnt = len(heads)
    msg = [{}] * msg_cnt
    for i in range(msg_cnt):
        head_split = heads[i].split(' ')
        if len(head_split[1]) != 8:
            head_split[1] = '0' + head_split[1]

        msg[i] = {
            'time': time.strptime(' '.join(head_split[:2]), '%Y-%m-%d %H:%M:%S'),
            'source': ' '.join(head_split[2:]).replace('\n', ''),
            'content': contents[i],
        }

    return msg


def split_txt(txt, max_cnt=0):
    re_target_head = r'={64}\n消息分组:.+?\n={64}\n消息对象:.+?\n={64}\n'
    heads = re.findall(re_target_head, txt)
    contents = re.split(re_target_head, txt)[1:]

    assert len(heads) == len(contents)

    sessions_cnt = len(heads)
    if max_cnt > 0:
        sessions_cnt = min(sessions_cnt, max_cnt)

    sessions = [{}] * sessions_cnt
    for i in range(sessions_cnt):
        head_split = re.split(r'={64}', heads[i])
        sessions[i] = {
            'group': head_split[1].replace('消息分组:', '').replace('\n', ''),
            'target': head_split[2].replace('消息对象:', '').replace('\n', ''),
            'msg': split_content(contents[i])
        }

        print('reading:', str(round(i / sessions_cnt * 100, 2)) + '%', sessions[i]['target'])
        sys.stdout.flush()

    return sessions


def main():
    with open('./configs.yaml', 'r') as f:
        configs = yaml.load(f.read(), Loader=yaml.Loader)

    with open(configs['file_path'], 'r') as f:
        s = f.read()
        s = s.replace('[图片]', '').replace('[表情]', '')

    start_time = time.strptime(configs['start_time'], '%Y-%m-%d %H:%M:%S')
    end_time = time.strptime(configs['end_time'], '%Y-%m-%d %H:%M:%S')

    sessions = split_txt(s)
    sessions_cnt = len(sessions)
    word_count = {}
    processed = 0
    for i in sessions:
        for j in i['msg']:
            if j['source'] != configs['user_name']:
                continue
            if start_time <= j['time'] < end_time:
                words = pseg.cut(j['content'])
                for k, pt in words:
                    if len(k) == 1:
                        continue
                    if k not in word_count:
                        word_count[k] = 1
                    else:
                        word_count[k] = word_count[k] + 1

        processed = processed + 1
        print('processing:', str(round(processed / sessions_cnt * 100, 2)) + '%')
        sys.stdout.flush()

    with open('./result.txt', 'w') as f:
        for i in sorted(word_count.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
            f.write(str(i) + '\n')

    wc = WordCloud(width=1280, height=720,
                   font_path='/home/cdcq/Downloads/SmileySans-Oblique.ttf',
                   background_color='white', max_words=100)
    wc.generate_from_frequencies(word_count)
    wc.to_file('./example.png')


def test():
    a = pseg.cut('说藏话了，妈妈生的')
    for i, j in a:
        print(i, j)


if __name__ == '__main__':
    main()
    # test()
