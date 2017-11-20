def synagogue_format(synagogue):
    synagogue_src = synagogue["_source"]
    return {
        "id": synagogue["_id"],
        "address": synagogue_src["address"],
        "classes": synagogue_src['classes'],
        "geo": synagogue_src['geo'],
        "name": synagogue_src['name'],
        "nosach": synagogue_src['nosach'],
        "parking": synagogue_src['parking'],
        "sefer-tora": synagogue_src['sefer-tora'],
        "wheelchair-accessible": synagogue_src['wheelchair-accessible'],
        "minyans": synagogue_src['minyans'],
        "comments": synagogue_src['comments']
    }
