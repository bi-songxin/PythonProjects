# 目标网址 https://zh.airbnb.com/

import requests
import jmespath
import pandas as pd
import pprint
# from curl_cffi import requests
headers = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'referer':'https://zh.airbnb.com/',
    'cookie':'_user_attributes=%7B%22curr%22%3A%22HKD%22%7D; bev=1781166570_EAOGUwOWE5NTJkMT; everest_cookie=1781166570.EAMTliMjY0OGI4ZDQ2NT.iuBxBqEtm5ACHaU6_z-ZciU1htpf6sdmDNb03BKaDSE; country=HK; _cci=cban%3Aac-8f5382a8-eb85-472c-b916-d92bd47d5d43; _ccv=cban%3A0_183215%3D1%2C0_200000%3D1%2C0_183345%3D1%2C0_183243%3D1%2C0_183216%3D1%2C0_179751%3D1%2C0_200003%3D1%2C0_200005%3D1%2C0_179750%3D1%2C0_179737%3D1%2C0_179744%3D1%2C0_179739%3D1%2C0_179743%3D1%2C0_179749%3D1%2C0_200011%3D1%2C0_183217%3D1%2C0_183219%3D1%2C0_179747%3D1%2C0_179740%3D1%2C0_179752%3D1%2C0_183241%3D1%2C0_200007%3D1%2C0_210000%3D1%2C0_210001%3D1%2C0_210002%3D1%2C0_210003%3D1%2C0_210004%3D1%2C0_210010%3D1%2C0_210012%3D1%2C0_210008%3D1%2C0_210016%3D1%2C0_210017%3D1%2C0_210018%3D1%2C0_210020%3D1%2C0_210021%3D1%2C0_210022%3D1%2C0_210026%3D1%2C0_210027%3D1; _gcl_au=1.1.3265629.1781166578; _ga=GA1.1.1250082454.1781166579; FPID=FPID2.2.gmnrwHsUoePMVqi6FYbxv6KssdLglu%2FILwdwVtH6iUQ%3D.1781166579; FPAU=1.1.3265629.1781166578; _scid=2ad27bc0-f180-47bc-f5c2-2023c7594534; __ps_r=_; __ps_lu=https://zh.airbnb.com/; __ps_fva=1781166581296; tzo=480; _gtmeec=eyJleHRlcm5hbF9pZCI6IjE3ODExNjY1NzBfRUFPR1V3T1dFNU5USmtNVCJ9; previousTab=%7B%22id%22%3A%225b3973c7-b96d-4af7-8dbf-2e9914d47763%22%7D; FPLC=D9pUSg0qcrjsh8FXz46guZv7tGlZSsSYIu9tKS8uxtKfgY7hw7%2BQLdPcaw%2FYG5vTjirca%2B6MPgjgwcazTKAAHc0UKSFrsmt3kEfxx%2B%2BjXnZiHfbSx%2B2urXvqLkiF4A%3D%3D; cfrmfctr=MOBILE; cbkp=1; frmfctr=compact; ak_bmsc=FAEEBEB5A02D4A6DD774C66BB19DA60A~000000000000000000000000000000~YAAQTVDGyyhYIImeAQAASG6cuwBOcX6FwohCAwmBint2cBWgTK3w/Pd5B3OTVKvHArvQps/25zZT3sGM5YsHFhnk8bKmIuGD9yihgEcKuMx3p8vmX077sPd/qElKYi0wZU3H3m+fBra+0P8/2C6l6NMv0+yVA0hZtDItXVL3pbLXzb9fHKmnspOQ8CToClkEsb4YPOHQlgwoSFpNgcgcm9Krs7I+72pJ8p3cMIlluDFpoHg5v+iOS7Ps+y8tYRdGLflqcL2aqSiFv7LBay7dueruv1GxpMzDuAU1gVmh3U9xX/L3gvcGLUCRbRJKdJXfIgVmSNtlwpERp2QqKS1QRvVATd6VSoxdNmJ99wtlOpeDB6DHB9v1vgs4FgrD22ieLK0KMKfpVB3NW2OW; jitney_client_session_id=694d295f-9525-464b-bc03-54e2a04f7479; jitney_client_session_created_at=1781264067.342; jitney_client_session_updated_at=1781264067.342; __ps_sr=_; __ps_slu=https://zh.airbnb.com/s/%E5%A4%A7%E9%98%AA%E5%B8%82/homes?place_id=ChIJ4eIGNFXmAGAR5y9q5G7BW8U&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=weekend_trip&date_picker_type=FLEXIBLE_DATES&search_type=HOMEPAGE_CAROUSEL_CLICK; __ps_did=pscrb_0f64ceed-060d-45d1-89a1-fd8790aadefa; _ga_2P6Q8PGG16=GS2.1.s1781264078$o6$g1$t1781264096$j42$l0$h99690718; datadome=rfgu7lIMbdIR7ZPFbqVe0DZl3CpcmRY1HynStOGC5u9rccUdf3frtOTsdoIPwtDEKXgCloLZMccwQ~9jpiqIfac0~TSfOGs3Q9cU7yW0mwqFisvm1iiC~rjwD2jFnmuY05XIcJTQ4_7JgRdgmToc40',
    'content-type':'application/json',
    'x-airbnb-api-key':'d306zoyjsyarp7ifhu67rjxn52tv0t20'
}

data = {
    "operationName": "StaysSearch",
    "variables": {
        "staysSearchRequest": {
            "metadataOnly": False,
            "requestedPageType": "STAYS_SEARCH",
            "searchType": "HOMEPAGE_CAROUSEL_CLICK",
            "treatmentFlags": [
                "feed_map_decouple_m11_treatment",
                "recommended_amenities_2024_treatment_b",
                "filter_redesign_2024_treatment",
                "filter_reordering_2024_roomtype_treatment",
                "p2_category_bar_removal_treatment",
                "selected_filters_2024_treatment",
                "recommended_filters_2024_treatment_b",
                "m13_search_input_phase2_treatment",
                "m13_search_input_services_enabled",
                "m13_2025_experiences_p2_treatment"
            ],
            "maxMapItems": 9999,
            "rawParams": [
                {
                    "filterName": "cdnCacheSafe",
                    "filterValues": [
                        "False"
                    ]
                },
                {
                    "filterName": "datePickerType",
                    "filterValues": [
                        "FLEXIBLE_DATES"
                    ]
                },
                {
                    "filterName": "flexibleTripLengths",
                    "filterValues": [
                        "weekend_trip"
                    ]
                },
                {
                    "filterName": "itemsPerGrid",
                    "filterValues": [
                        "18"
                    ]
                },
                {
                    "filterName": "placeId",
                    "filterValues": [
                        "ChIJ4eIGNFXmAGAR5y9q5G7BW8U"
                    ]
                },
                {
                    "filterName": "query",
                    "filterValues": [
                        "大阪市"
                    ]
                },
                {
                    "filterName": "refinementPaths",
                    "filterValues": [
                        "/homes"
                    ]
                },
                {
                    "filterName": "screenSize",
                    "filterValues": [
                        "small"
                    ]
                },
                {
                    "filterName": "tabId",
                    "filterValues": [
                        "home_tab"
                    ]
                },
                {
                    "filterName": "version",
                    "filterValues": [
                        "1.8.8"
                    ]
                }
            ]
        },
        "staysMapSearchRequestV2": {
            "metadataOnly": False,
            "requestedPageType": "STAYS_SEARCH",
            "searchType": "HOMEPAGE_CAROUSEL_CLICK",
            "treatmentFlags": [
                "feed_map_decouple_m11_treatment",
                "recommended_amenities_2024_treatment_b",
                "filter_redesign_2024_treatment",
                "filter_reordering_2024_roomtype_treatment",
                "p2_category_bar_removal_treatment",
                "selected_filters_2024_treatment",
                "recommended_filters_2024_treatment_b",
                "m13_search_input_phase2_treatment",
                "m13_search_input_services_enabled",
                "m13_2025_experiences_p2_treatment"
            ],
            "rawParams": [
                {
                    "filterName": "cdnCacheSafe",
                    "filterValues": [
                        "False"
                    ]
                },
                {
                    "filterName": "datePickerType",
                    "filterValues": [
                        "FLEXIBLE_DATES"
                    ]
                },
                {
                    "filterName": "flexibleTripLengths",
                    "filterValues": [
                        "weekend_trip"
                    ]
                },
                {
                    "filterName": "placeId",
                    "filterValues": [
                        "ChIJ4eIGNFXmAGAR5y9q5G7BW8U"
                    ]
                },
                {
                    "filterName": "query",
                    "filterValues": [
                        "大阪市"
                    ]
                },
                {
                    "filterName": "refinementPaths",
                    "filterValues": [
                        "/homes"
                    ]
                },
                {
                    "filterName": "screenSize",
                    "filterValues": [
                        "small"
                    ]
                },
                {
                    "filterName": "tabId",
                    "filterValues": [
                        "home_tab"
                    ]
                },
                {
                    "filterName": "version",
                    "filterValues": [
                        "1.8.8"
                    ]
                }
            ]
        },
        "isLeanTreatment": False,
        "aiSearchEnabled": False
    },
    "extensions": {
        "persistedQuery": {
            "version": 1,
            "sha256Hash": "b9389bf17721a08edbea5073307d377d39325b2e4acaf008e87d847a2e112cf8"
        }
    }
}

url = 'https://zh.airbnb.com/api/v3/StaysSearch/b9389bf17721a08edbea5073307d377d39325b2e4acaf008e87d847a2e112cf8'
resp = requests.post(url,headers = headers,json = data)
resp_data = resp.json()
# 🎯 编写 JMESPath 路径表达式，跨越十几层嵌套，直接批量提取所有房源信息（完全免去 for 循环！）
expression = """
data.presentation.staysSearch.results.searchResults[*].{
    "标题": title,
    "描述": subtitle,
    "评分": avgRatingLocalized,
    "总价": structuredDisplayPrice.primaryLine.price,
    "周期": structuredDisplayPrice.primaryLine.qualifier,
    "纬度": demandStayListing.location.coordinate.latitude,
    "经度": demandStayListing.location.coordinate.longitude
}
"""

# 一行代码，全部抽离
clean_listings = jmespath.search(expression, resp_data)
total_count_home = len(clean_listings)
print(f"================ 成功抓取到 {total_count_home} 家房源信息 ================")
# 打印出来看看，结构会变得极其清爽！
print(clean_listings)
print('---'*50)
pprint.pprint(clean_listings)

df = pd.DataFrame(clean_listings)
df.to_excel("大阪房源数据.xlsx", index=False)

# tls指纹检查网址
# url2 = 'https://tls.browserleaks.com/json'
#
# resp2 = requests.get(url2,headers=headers)
# print(resp2.text)