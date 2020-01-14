# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SweetwaterItem(scrapy.Item):
    G_Manufacturer = scrapy.Field()
    G_MPN = scrapy.Field()
    G_MSRP = scrapy.Field()
    G_SALE_NEW = scrapy.Field()
    G_Body_Type = scrapy.Field()
    G_Body_Shape_Spec = scrapy.Field()
    G_Left_Handed = scrapy.Field()
    G_Number_Of_Strings = scrapy.Field()
    G_Body_Material = scrapy.Field()
    G_Top_Material = scrapy.Field()
    G_Body_Finish = scrapy.Field()
    G_Color = scrapy.Field()
    G_Neck_Material = scrapy.Field()
    G_Neck_Shape = scrapy.Field()
    G_Radius = scrapy.Field()
    G_Fingerboard_Material = scrapy.Field()
    G_Fingerboard_Inlay = scrapy.Field()
    G_Number_Of_Frets = scrapy.Field()
    G_Scale_Length = scrapy.Field()
    G_Nut_Width = scrapy.Field()
    G_Nut_Material = scrapy.Field()
    G_Bridge = scrapy.Field()
    G_Tuners = scrapy.Field()
    G_Neck_Pickup = scrapy.Field()
    G_Middle_Pickup = scrapy.Field()
    G_Bridge_Pickup = scrapy.Field()
    G_Controls = scrapy.Field()
    G_Strings = scrapy.Field()
    G_Case_Included = scrapy.Field()
    G_Bridge_Type = scrapy.Field()
    G_Body_Shape_Filter = scrapy.Field()
    G_Source = scrapy.Field()
