from playwright.sync_api import sync_playwright
from app.logger import logger
from app.db.database import SessionLocal
from app.db.models.product import Catalog, Product


class Parser:
    def __init__(self, base_url):
        self.playwright = sync_playwright().start()
        browser = self.playwright.chromium.launch(headless=True)

        self.browser = browser
        self.page = browser.new_page()
        self.url = base_url
        self.db = SessionLocal()
    
    def close(self):
        self.browser.close()
        self.playwright.stop()
        self.db.close()
    
    def __str__(self):
        return f"Parser for {self.url}"
    
    def get_catalog(self):
        link = self.url + "/catalog/"
        self.page.goto(self.url + "/catalog/")
        self.page.wait_for_load_state("networkidle")
        links = self.page.query_selector_all('.widget-element-name.intec-cl-text-hover')
        logger.info(f"Found {len(links)} catalog links.")

        catalogs = []

        for link in links:
            href = link.get_attribute('href')
            title = link.text_content().strip()

            # DB'da mavjudligini tekshirish
            existing_catalog = self.db.query(Catalog).filter(Catalog.link == href).first()

            if existing_catalog:
                # Agar mavjud bo'lsa, uni ishlatish
                catalog = existing_catalog
                logger.info(f"Catalog already exists in DB: {title} (ID: {catalog.id})")
            else:
                # Yangi katalog qo'shish
                catalog = Catalog(name=title, link=href)
                self.db.add(catalog)
                self.db.commit()
                self.db.refresh(catalog)
                logger.info(f"Saved new catalog to DB: {title} (ID: {catalog.id})")

            catalogs.append({'id': catalog.id, 'href': href, 'title': title})

        logger.info(f"Extracted and saved {len(catalogs)} catalogs to database.")

        return catalogs
                
    def parse_catalog(self, url, catalog_id):
        self.page.goto(self.url + url)
        products = []

        tr = self.page.query_selector_all(".main-catalog>tbody>tr")
        brand = None

        for index, row in enumerate(tr, start=1):
            tds = row.query_selector_all("td")
            count = len(tds)

            if count == 3:
                logger.info(f"Parse index: {index}, title: {tds[0].get_attribute('data-name')}")
                brand = tds[0].get_attribute('data-name')

            product = row.query_selector(".product-name>a")

            if product:
                product_name = product.text_content().strip()
                href = product.get_attribute('href')
                full_url = self.url + href if href else None
                desc = tds[-1].text_content().strip() if href else None

                # DB'da mavjudligini tekshirish
                existing_product = self.db.query(Product).filter(Product.link == full_url).first()

                if existing_product:
                    # Agar mavjud bo'lsa, skip qilish
                    logger.info(f"Product already exists in DB: {product_name} (ID: {existing_product.id})")
                    products.append({'brand': brand, 'product_name': product_name, 'link': full_url, 'description': desc})
                else:
                    # Yangi product qo'shish
                    product_db = Product(
                        catalog_id=catalog_id,
                        brand=brand,
                        model=product_name,
                        link=full_url,
                        description=desc
                    )
                    self.db.add(product_db)
                    self.db.commit()
                    self.db.refresh(product_db)

                    products.append({'brand': brand, 'product_name': product_name, 'link': full_url, 'description': desc})
                    logger.info(f"Saved new product to DB: {product_name} (ID: {product_db.id})")

        logger.info(f"Total products found and saved: {len(products)}")
        return products