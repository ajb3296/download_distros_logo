import os
import shutil
import requests
import multiprocessing
from bs4 import BeautifulSoup

from modules.get_logo import get_logos

if __name__ == "__main__":
    image_path = "images"
    link = "https://distrowatch.com/search.php?ostype=Linux&category=All&origin=All&basedon=All&notbasedon=None&desktop=All&architecture=All&package=All&rolling=All&isosize=All&netinstall=All&language=All&defaultinit=All&status=All#simple"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}

    # 이미지를 저장할 폴더 생성
    try:
        shutil.rmtree(image_path)
    except FileNotFoundError:
        pass
    os.mkdir(image_path)

    print("GETTING DISTROS LIST. . .") # Getting distros list

    req = requests.get(link, headers=header)
    soup = BeautifulSoup(req.text, "lxml")

    result = soup.find("table", {"class": "Logo"}).find("table", {"class": "News"}).find_all("td", {"class": "NewsText"})[1]
    # 필요없는 데이터 제거
    result.find("table").clear()
    result.find("b").clear()

    result = result.find_all("b")

    # 링크 추출
    distros = []
    for distro in result:
        link = distro.find("a")
        if link is not None:
            l = str(link["href"]).strip()
            if l != "":
                distros.append(l)
    
    print("DOWNLOAD DISTROS LOGO IMAGE. . .")
    print("DISTROS COUNT: " + str(len(distros)))

    distro_per_process = 20
    # 이미지 다운로드
    process_list = []
    for num in range(int(len(distros) / distro_per_process)):
        first_num = num * distro_per_process
        last_num = first_num + distro_per_process - 1
        
        process = multiprocessing.Process(target=get_logos, args=(distros[first_num:last_num]))
        process.start()
        process_list.append(process)
    
    if len(distros) % distro_per_process != 0:
        process = multiprocessing.Process(target=get_logos, args=(distros[last_num + 1:]))
        process.start()
        process_list.append(process)

    for process in process_list:
        process.join()
    
    print("FINISH!")