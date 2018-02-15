def synagogue_format(synagogue):
    synagogue_src = synagogue["_source"]
    return {
        "id": synagogue["_id"],
        "geo": synagogue_src['geo'],
        "name": synagogue_src['name'],
        "address": synagogue_src.get("address"),
        "classes": synagogue_src.get('classes'),
        "nosach": synagogue_src.get('nosach'),
        "parking": synagogue_src.get('parking'),
        "sefer-tora": synagogue_src.get('sefer-tora'),
        "wheelchair-accessible": synagogue_src.get('wheelchair-accessible'),
        "minyans": synagogue_src.get('minyans'),
        "comments": synagogue_src.get('comments')
    }
