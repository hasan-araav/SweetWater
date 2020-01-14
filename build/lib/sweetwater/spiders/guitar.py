# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from sweetwater.items import SweetwaterItem
import lxml
import re


class GuitarSpider(scrapy.Spider):
    name = "guitar"
    base_url = 'sweetwater.com'
    allowed_domains = [base_url]
    schemed_base_url = 'https://' + base_url
    start_urls = [schemed_base_url + '/c590--Les_Paul_Solidbody_Guitars?params=eyJmYWNldCI6eyJCcmlkZ2VcL1RhaWxwaWVjZSI6WyJGaXhlZCJdfX0']
    item_limit = 1             # the limit for number of items to crawl
    crawled_items_count = 0     # counter for the items crawled so far

    def parse(self, response):
        """
        Parses an item list page.
        """
        if response is None:
            return None

        # if self.crawled_items_count > self.item_limit:
        #     return

        soup = BeautifulSoup(response.body, 'lxml')

        body_shape_ul = soup.find("ul", attrs={"filtertype":"Body_Shape"})
        body_shape_filter_text = []
        if body_shape_ul:
            body_shape_li = body_shape_ul.find_all("li", "checked")
            if body_shape_li:
                for li in body_shape_li:
                    body_shape_filter_text.append(li.a.span.text)

        body_shape_filter_text = ','.join(body_shape_filter_text)

        # first, yield a request for the next item list page (for better parallalization)
        next_page_link = soup.find('a', {'class' : 'next'})
        if next_page_link:
            next_page_url = self.schemed_base_url + next_page_link.get('href')
            yield scrapy.Request(url=next_page_url, callback=self.parse)

        # yield requests for the item pages
        for product_html in soup.find_all('div', {'class' : 'product-card'}):
            # if self.crawled_items_count > self.item_limit:
            #     return

            if (product_html is None) or (product_html.a is None):
                continue

            self.crawled_items_count += 1
            item_link = self.schemed_base_url + product_html.a.get('href')

            yield scrapy.Request(item_link, callback=self.parse_item, meta={'body_shape_filter': body_shape_filter_text})

    def parse_item(self, response):
        """
        Parses a single item.
        """
        soup = BeautifulSoup(response.body, 'lxml')

        specs = soup.select('.product-specs .table__cell')

        item = SweetwaterItem()

        manufacturer = soup.find(attrs={"name":"manufacturer"})
        if manufacturer:
            item['G_Manufacturer'] = ''.join(manufacturer['value'])
        else:
            item['G_Manufacturer'] = ''

        product_id = soup.find('span', {'itemprop' : 'productID'})
        if product_id:
            item['G_MPN'] = product_id.text
        else:
            item['G_MPN'] = ''

        msrp = soup.find('span','product-pricing-line--base')
        if msrp:
            item['G_MSRP'] = msrp.price.text
        else:
            item['G_MSRP'] = ''

        sale_price = soup.find('price')
        if sale_price:
            item['G_SALE_NEW'] = sale_price.text
        else:
            item['G_SALE_NEW'] = ''

        body_type = soup.find("strong", string=re.compile("Body Type:"))
        if body_type:
            item['G_Body_Type'] = ''.join(body_type.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Body_Type'] = ''

        body_shape_spec = soup.find("strong", string=re.compile("Body Shape:"))
        if body_shape_spec:
            item['G_Body_Shape_Spec'] = ''.join(body_shape_spec.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Body_Shape_Spec'] = ''

        left_handed = soup.find("strong", string=re.compile("Left-/Right-handed:"))
        if left_handed:
            item['G_Left_Handed'] = ''.join(left_handed.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Left_Handed'] = ''

        number_of_strings = soup.find("strong", string=re.compile("Number of Strings:"))
        if number_of_strings:
            item['G_Number_Of_Strings'] = ''.join(number_of_strings.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Number_Of_Strings'] = ''

        body_material = soup.find("strong", string=re.compile("Body Material:"))
        if body_material:
            item['G_Body_Material'] = ''.join(body_material.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Body_Material'] = ''

        top_material = soup.find("strong", string=re.compile("Top Material:"))
        if top_material:
            item['G_Top_Material'] = ''.join(top_material.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Top_Material'] = ''

        body_finish = soup.find("strong", string=re.compile("Body Finish:"))
        if body_finish:
            item['G_Body_Finish'] = ''.join(body_finish.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Body_Finish'] = ''

        color = soup.find("strong", string=re.compile("Color:"))
        if color:
            item['G_Color'] = ''.join(color.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Color'] = ''

        neck_material = soup.find("strong", string=re.compile("Neck Material:"))
        if neck_material:
            item['G_Neck_Material'] = ''.join(neck_material.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Neck_Material'] = ''

        neck_shape = soup.find("strong", string=re.compile("Neck Shape:"))
        if neck_shape:
            item['G_Neck_Shape'] = ''.join(neck_shape.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Neck_Shape'] = ''

        radius = soup.find("strong", string=re.compile("Radius:"))
        if radius:
            item['G_Radius'] = ''.join(radius.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Radius'] = ''

        fingerboard_material = soup.find("strong", string=re.compile("Fingerboard Material:"))
        if fingerboard_material:
            item['G_Fingerboard_Material'] = ''.join(fingerboard_material.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Fingerboard_Material'] = ''

        fingerboard_inlay = soup.find("strong", string=re.compile("Fingerboard Inlay:"))
        if fingerboard_inlay:
            item['G_Fingerboard_Inlay'] = ''.join(fingerboard_inlay.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Fingerboard_Inlay'] = ''

        number_of_freets = soup.find("strong", string=re.compile("Number of Frets:"))
        if number_of_freets:
            item['G_Number_Of_Frets'] = ''.join(number_of_freets.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Number_Of_Frets'] = ''

        scale_length = soup.find("strong", string=re.compile("Scale Length:"))
        if scale_length:
            item['G_Scale_Length'] = ''.join(scale_length.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Scale_Length'] = ''

        nut_width = soup.find("strong", string=re.compile("Nut Width:"))
        if nut_width:
            item['G_Nut_Width'] = ''.join(nut_width.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Nut_Width'] = ''

        nut_material = soup.find("strong", string=re.compile("Nut Material:"))
        if nut_material:
            item['G_Nut_Material'] = ''.join(nut_material.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Nut_Material'] = ''

        bridge = soup.find("strong", string=re.compile("Bridge/Tailpiece:"))
        if bridge:
            item['G_Bridge'] = ''.join(bridge.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Bridge'] = ''

        tuners = soup.find("strong", string=re.compile("Tuners:"))
        if tuners:
            item['G_Tuners'] = ''.join(tuners.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Tuners'] = ''

        neck_pickup = soup.find("strong", string=re.compile("Neck Pickup:"))
        if neck_pickup:
            item['G_Neck_Pickup'] = ''.join(neck_pickup.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Neck_Pickup'] = ''

        middle_pickup = soup.find("strong", string=re.compile("Middle Pickup:"))
        if middle_pickup:
            item['G_Middle_Pickup'] = ''.join(middle_pickup.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Middle_Pickup'] = ''

        bridge_pickup = soup.find("strong", string=re.compile("Bridge Pickup:"))
        if bridge_pickup:
            item['G_Bridge_Pickup'] = ''.join(bridge_pickup.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Bridge_Pickup'] = ''

        controls = soup.find("strong", string=re.compile("Controls:"))
        if controls:
            item['G_Controls'] = ''.join(controls.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Controls'] = ''

        strings = soup.find("strong", string=re.compile("Strings:"))
        if strings:
            item['G_Strings'] = ''.join(strings.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Strings'] = ''

        case_included = soup.find("strong", string=re.compile("Case Included:"))
        if case_included:
            item['G_Case_Included'] = ''.join(case_included.find_next_sibling("span", "table__cell")).strip()
        else:
            item['G_Case_Included'] = ''

        item['G_Bridge_Type'] = ''
        item['G_Body_Shape_Filter'] = response.meta['body_shape_filter']
        item['G_Source'] = 'SweetWater'
        return item
