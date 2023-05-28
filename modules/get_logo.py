import time
import requests

def get_logos(*logo_list):
    img_link_base = "https://distrowatch.com/images/yvzhuwbpy/"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}

    img_path = "images/"

    err_count = 0

    for logo in logo_list:
        try:
            img_link = img_link_base + logo + ".png"
        except:
            print("ERROR")
            print(logo)

        try:
            f = open(img_path + logo + ".png", 'wb')
            response = requests.get(img_link, headers=header)
            f.write(response.content)
            f.close()
        except:
            print(f"Error: {img_link}")
            err_count += 1

        
        time.sleep(10)
    
    print(f"Error count({logo_list[0]} to {logo_list[-1]}): {err_count}")
