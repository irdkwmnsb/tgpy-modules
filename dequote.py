"""
    name: dequote
    once: false
    origin: tgpy://module/dequote
    priority: 1676719918.238895
    save_locals: true
"""
tgpy.add_code_transformer('dequote', lambda x: x.replace("”", '"').replace("“", '"').replace("‘", "'").replace("’", "'"))
