def synagogue_format(synagogue):
    synagogue_src = synagogue["_source"]
    return {
        "id": synagogue["_id"],
        "geo": {'lat': float(synagogue_src['geo']['lat']), 'lon': float(synagogue_src['geo']['lon'])},
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

def kehilot_format(synagogue):
    x = synagogue_format(synagogue)
    x["kehilot-display"] = synagogue["_source"].get('kehilot-display')
    return x