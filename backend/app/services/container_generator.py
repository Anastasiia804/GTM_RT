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
    """Basic JavaScript minification - removes comments and extra whitespace
    Note: This is a simple minification. For production, consider using a proper
    JS minifier library like jsmin or integrating with a build tool.
    """
    lines = []
    in_string = False
    string_char = None
    
    for line in code.split('\n'):
        cleaned = []
        i = 0
        while i < len(line):
            char = line[i]
            
            # Track string state to avoid removing // inside strings
            if char in ('"', "'") and (i == 0 or line[i-1] != '\\'):
                if not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char:
                    in_string = False
                    string_char = None
            
            # Remove comments only when not in a string
            if not in_string and i < len(line) - 1:
                if line[i:i+2] == '//':
                    break
            
            cleaned.append(char)
            i += 1
        
        lines.append(''.join(cleaned).strip())
    
    # Join and remove extra whitespace
    minified = ' '.join(lines)
    minified = ' '.join(minified.split())
    
    return minified
