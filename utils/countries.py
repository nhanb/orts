import pycountry


def country_name_to_code(name, cache={"South Korea": "kr"}):
    # None, empty string:
    if not name:
        return None

    if name in cache:
        return cache[name]

    try:
        code = pycountry.countries.lookup(name).alpha_2.lower()
        cache[name] = code
        return code
    except LookupError:
        print(f"Country not found: {name}")
        return None
