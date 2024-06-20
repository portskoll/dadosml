import scrapy
import re


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]
    page_count = 1
    max_pages = 10

    def parse(self, response):
        products =  response.css('div.ui-search-result__content')

        for product in products:

            brand = product.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get()
            # Extrai o número de avaliações e a quantidade de reviews
            reviews_rating_number = product.css('span.ui-search-reviews__rating-number::text').get()
            reviews_amount = product.css('span.ui-search-reviews__amount::text').get()

            # Verifica se os valores são None e substitui por '0'
            reviews_rating_number = reviews_rating_number if reviews_rating_number else '0.0'
            reviews_amount = reviews_amount if reviews_amount else '(0)'
            brand = brand if brand else 'sem marca'
            

            yield {
                'brand': brand,
                'name': product.css('h2.ui-search-item__title::text').get(),
                'reviews_rating_number': reviews_rating_number,
                'reviews_amount': reviews_amount,
                #'price': product.css('span.andes-money-amount[style="font-size:24px"][aria-label]::attr(aria-label)').re_first(r'(\d+ reais com \d+ centavos)')
                'price': product.css('span.andes-money-amount[style="font-size:24px"][aria-label]::attr(aria-label)').re_first(r'(\d+) reais(?: com (\d+) centavos)?', lambda m: f"{m.group(1)}.{m.group(2) if m.group(2) else '00'}")
                
            }
        if self.page_count < self.max_pages:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)


