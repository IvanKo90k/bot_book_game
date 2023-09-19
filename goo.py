from icrawler.builtin import GoogleImageCrawler

def google_img_downloader():
    filters = dict(
        size='large',
        license='noncommercial'
    )
    crawler = GoogleImageCrawler(storage={'root_dir': './img'})
    crawler.crawl(keyword='pinterest farmland',
                  max_num=5,
                  min_size=(1000,1000),
                  overwrite=True,
                  filters=filters,
                  file_idx_offset='auto'
    )

def main():
    google_img_downloader()

if __name__ == '__main__':
    main()