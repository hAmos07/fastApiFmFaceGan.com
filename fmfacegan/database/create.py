def record_xml_create(ids: list) -> str:
    record_list = list()

    graphics_template = '''<record>
    <boolean id="preload" value="false"/>
    <boolean id="amap" value="false"/>
    <list id="maps">
    {RECORDS}
    </list>
    </record>'''

    for regen_id in ids:
        record = f'<record from="{regen_id}" to="graphics/pictures/person/{regen_id}/portrait"/>'
        record_list.append(record)
    result = '\n'.join(record_list)

    graphics_template = graphics_template.replace('{RECORDS}', result)
    return graphics_template
