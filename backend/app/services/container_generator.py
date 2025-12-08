from sqlalchemy.orm import Session
from ..models.advertiser import Advertiser
from ..models.script import Script
import json


def generate_container_code(advertiser: Advertiser) -> str:
    """Generate the container embed code for an advertiser"""
    code = f'''<!-- TSPRTG Container for: {advertiser.name} -->
<!-- Container ID: {advertiser.container_id} -->
<script type="text/javascript">
(function(w,d,c){{
    var r=d.readyState;
    if(r!=='interactive'&&r!=='complete'){{
        return setTimeout(function(){{arguments.callee(w,d,c)}},100);
    }}
    var s=d.createElement('script');
    s.async=true;
    s.src='//tsprtg.com/c/'+c+'/l.js?v='+(+new Date());
    (d.body||d.head).appendChild(s);
    w._tsprtg=w._tsprtg||{{}};
    w._tsprtg.cid=c;
}})(window,document,'{advertiser.container_id}');
</script>
<!-- End TSPRTG Container -->'''
    return code


def generate_loader_script(db: Session, advertiser: Advertiser) -> str:
    """Generate the loader JavaScript that will be served at /c/{container_id}/l.js"""
    
    # Get global scripts (advertiser_id is NULL)
    global_scripts = db.query(Script).filter(
        Script.advertiser_id.is_(None),
        Script.is_enabled == True
    ).order_by(Script.priority).all()
    
    # Get advertiser-specific scripts
    advertiser_scripts = db.query(Script).filter(
        Script.advertiser_id == advertiser.id,
        Script.is_enabled == True
    ).order_by(Script.priority).all()
    
    # Combine scripts
    all_scripts = global_scripts + advertiser_scripts
    
    # Generate JavaScript code
    js_code = "(function(){\n"
    js_code += "'use strict';\n"
    js_code += f"console.log('TSPRTG Container loaded: {advertiser.container_id}');\n"
    
    for script in all_scripts:
        if script.script_type == 'external':
            # Load external script
            async_attr = "s.async=true;" if script.is_async else ""
            defer_attr = "s.defer=true;" if script.is_defer else ""
            js_code += f"""
var s=document.createElement('script');
s.src='{script.content}';
{async_attr}
{defer_attr}
(document.body||document.head).appendChild(s);
"""
        elif script.script_type == 'inline':
            # Execute inline script
            js_code += f"\n// Script: {script.name}\n"
            js_code += f"{script.content}\n"
    
    js_code += "})();\n"
    
    return js_code


def minify_js(code: str) -> str:
    """Basic JavaScript minification"""
    # Remove comments
    lines = []
    for line in code.split('\n'):
        # Remove single-line comments
        if '//' in line:
            line = line[:line.index('//')]
        lines.append(line.strip())
    
    # Join and remove extra whitespace
    minified = ' '.join(lines)
    minified = ' '.join(minified.split())
    
    return minified
