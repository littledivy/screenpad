import pynput.keyboard as Keyboard
from pynput import mouse
import webview
import time
import _thread

permitted_chars = ["w", "a", "s", "d"]

layout = """
<html>
  <style>
  table, th {
    border-radius: 2px;
    text-align: center;
  }
  
  td {
    padding: 8px;
    background-color: #1b262c;
    color: #fff;
    opacity: 0.7;
    border: 1px solid #1b262c; 
    border-radius: 4px;
  }
  
  .noop {
    background-color: transparent!important; border: none;
  }
  
  #left, #right {
    font-size: .8rem;
  }
  </style>
  <body>
    <table width="100%" cellpadding="10">
       <tr>
         <td class="noop"></td>
         <td class="noop"></td>
         <td id="w" colspan="2">W</td>
         <td class="noop"></td>
         <td class="noop"></td>
       </tr>
      <tr>
        <td class="noop"></td>
        <td id="a">A</td>
        <td id="s" colspan="2">S</td>
        <td id="d">D</td>
        <td class="noop"></td>
      </tr>
      <tr>
         <td class="noop"></td>
         <td id="cps" colspan="4">
           <cps style="float: left">
             LMB <br>
             <cps id="left"> </cps>
           </cps>
           <cps style="float: right">
             RMB <br>
             <cps id="right"> </cps>
           </cps>
         </td>
         <td class="noop"></td>
      </tr>
      <tr>
        <td class="noop"></td>
        <td colspan="4" style="padding: 2px;" id="space">SPACE</td>
        <td class="noop"></td>
      </tr>
    </table>
  </body>
  <script>
    window.set_label = function(key, no_bg) {
      document.getElementById(key).style.opacity = 1;
      if(no_bg) return;
      document.getElementById(key).style.backgroundColor = "#fff"
      document.getElementById(key).style.color = "#1b262c"
    }
    window.clear_label = function(key) {
      document.getElementById(key).style.opacity = 0.7;
      document.getElementById(key).style.backgroundColor = "#1b262c"
      document.getElementById(key).style.color = "#fff"
    }
    window.set_cps = function(key, cps) {
      document.getElementById(key).innerHTML = cps + " cps"; 
    }
  </script>
</html>
"""

window = webview.create_window('Screenkey', html=layout, frameless=True, on_top=True, width=80, height=180, transparent=True)

right_cps = 0
left_cps = 0

def set_cps_js(td_id, cps):
  window.evaluate_js("window.set_cps('" + td_id + "', '"+ str(cps) +"')")

def reset_globals():
  global left_cps, right_cps
  left_cps = 0
  right_cps = 0
  set_cps_js("right", 0)
  set_cps_js("left", 0)

def update_cps(right):
  global left_cps, right_cps
  cps = 0
  if right:
    cps = left_cps + 1
    left_cps = cps
  else:
    cps = right_cps + 1
    right_cps = cps
  return cps

def trigger_js(key):
  return "window.set_label('" + key + "')"

def on_press(key):
    # Callback function whenever a key is pressed
    try:
        if key.char in permitted_chars:
          window.evaluate_js(trigger_js(key.char))
    except AttributeError:
        if key == Keyboard.Key.space:
          window.evaluate_js(trigger_js("space"))

def on_release(key):
    try:
      if key.char in permitted_chars:
        window.evaluate_js(f'window.clear_label({key})')
    except:
      if key == Keyboard.Key.space:
        window.evaluate_js(f'window.clear_label("space")')


def on_click(x, y, button, pressed):
    td_id = "left"
    if button == mouse.Button.left:
        td_id = "left"
    elif button == mouse.Button.right:
        td_id = "right"
    elif button == mouse.Button.middle:
        return
    
    if pressed:
      window.evaluate_js("window.set_label('" + td_id + "', true)")
      set_cps_js(td_id, update_cps(td_id == "right"))
    else:    
      window.evaluate_js("window.clear_label('" + td_id + "')")


def timer():
  reset_globals()
  time.sleep(1)
  timer()

_thread.start_new_thread(timer, ())

def listen():
  with Keyboard.Listener(on_press=on_press, on_release=on_release) as k_listener, \
  mouse.Listener(on_click=on_click) as m_listener:
      k_listener.join()
      m_listener.join()
      
      
    
webview.start(listen);

