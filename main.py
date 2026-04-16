#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, Gio, Gdk, GtkLayerShell
import os
import json

class AppLauncher(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        
        # Initialize layer shell
        GtkLayerShell.init_for_window(self)
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.OVERLAY)
        GtkLayerShell.set_keyboard_mode(self, GtkLayerShell.KeyboardMode.EXCLUSIVE)
        
        # Center window
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, False)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.BOTTOM, False)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, False)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, False)
        
        # Set explicit size
        self.set_size_request(1200, 800)
        self.set_default_size(1200, 800)
        
        # Load colors
        self.colors = self.load_colors()
        
        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.add(main_box)
        
        # Sidebar with background
        sidebar_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar_container.get_style_context().add_class("sidebar-container")
        sidebar_container.set_margin_start(20)
        sidebar_container.set_margin_end(12)
        sidebar_container.set_margin_top(28)
        sidebar_container.set_margin_bottom(28)
        
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        sidebar.set_size_request(100, -1)
        sidebar.set_valign(Gtk.Align.CENTER)
        sidebar.set_margin_start(8)
        sidebar.set_margin_end(8)
        sidebar.set_margin_top(16)
        sidebar.set_margin_bottom(16)
        
        categories = [
            ("apps", "All Apps", "all"),
            ("sports_esports", "Games", "Game"),
            ("code", "Development", "Development"),
            ("language", "Internet", "Network"),
            ("photo_library", "Media", "AudioVideo"),
        ]
        
        self.category_buttons = []
        for icon, label, cat in categories:
            btn = Gtk.Button()
            btn_box = Gtk.Box(spacing=0)
            btn_box.set_halign(Gtk.Align.CENTER)
            
            icon_label = Gtk.Label(label=icon)
            icon_label.get_style_context().add_class("material-icon")
            btn_box.pack_start(icon_label, True, True, 0)
            
            btn.add(btn_box)
            btn.get_style_context().add_class("category-btn")
            btn.set_tooltip_text(label)
            btn.connect("clicked", self.on_category_clicked, cat)
            btn.category = cat
            sidebar.pack_start(btn, False, False, 0)
            self.category_buttons.append(btn)
        
        self.category_buttons[0].get_style_context().add_class("active")
        self.current_category = "all"
        
        sidebar_container.pack_start(sidebar, True, False, 0)
        main_box.pack_start(sidebar_container, False, False, 0)
        
        # Content
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        content.set_margin_start(16)
        content.set_margin_end(28)
        content.set_margin_top(28)
        content.set_margin_bottom(28)
        
        # Search
        search_box = Gtk.Box(spacing=12)
        search_box.get_style_context().add_class("search-box")
        search_box.set_margin_start(16)
        search_box.set_margin_end(16)
        
        search_icon = Gtk.Label(label="search")
        search_icon.get_style_context().add_class("material-icon")
        search_box.pack_start(search_icon, False, False, 0)
        
        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Type to search...")
        self.search_entry.get_style_context().add_class("search-entry")
        self.search_entry.connect("changed", self.on_search_changed)
        search_box.pack_start(self.search_entry, True, True, 0)
        
        content.pack_start(search_box, False, False, 0)
        
        # Apps
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        
        self.flow = Gtk.FlowBox()
        self.flow.set_valign(Gtk.Align.START)
        self.flow.set_max_children_per_line(4)
        self.flow.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.flow.set_row_spacing(16)
        self.flow.set_column_spacing(16)
        self.flow.set_homogeneous(True)
        self.flow.set_can_focus(True)
        self.flow.connect("child-activated", self.on_flow_activated)
        
        scroll.add(self.flow)
        content.pack_start(scroll, True, True, 0)
        
        main_box.pack_start(content, True, True, 0)
        
        # Load apps
        self.apps = self.load_apps()
        self.update_apps()
        
        # CSS
        self.apply_css()
        
        # ESC to close
        self.connect("key-press-event", self.on_key_press)
    
    def load_colors(self):
        try:
            path = os.path.expanduser("~/.local/state/quickshell/user/generated/colors.json")
            with open(path) as f:
                data = json.load(f)
                colors = {}
                for key, value in data.items():
                    colors[key] = {"default": {"hex": value}}
                return colors
        except:
            return {
                "primary": {"default": {"hex": "#cbc3d5"}},
                "primary_container": {"default": {"hex": "#3f3849"}},
                "on_surface": {"default": {"hex": "#e6e1e3"}},
                "on_surface_variant": {"default": {"hex": "#c9c5c7"}},
            }
    
    def apply_css(self):
        c = self.colors
        bg_color = c.get('surface_container', {}).get('default', {}).get('hex', '#201f21')
        css = f"""
            window {{
                background: {bg_color};
                border-radius: 32px;
            }}
            .sidebar-container {{
                background: rgba(0, 0, 0, 0.3);
                border-radius: 28px;
            }}
            .category-btn {{
                background: transparent;
                border: none;
                border-radius: 20px;
                padding: 12px 8px;
                color: {c['on_surface_variant']['default']['hex']};
                font-family: "Google Sans";
                font-size: 14px;
                font-weight: 500;
            }}
            .category-btn:hover {{
                background: rgba(203, 195, 213, 0.2);
            }}
            .category-btn.active {{
                background: {c['primary_container']['default']['hex']};
                color: {c['primary']['default']['hex']};
            }}
            .material-icon {{
                font-family: "Material Symbols Rounded";
                font-size: 24px;
            }}
            .search-box {{
                background: rgba(0, 0, 0, 0.4);
                border-radius: 28px;
                padding: 10px 20px;
            }}
            .search-entry {{
                background: transparent;
                border: none;
                color: {c['on_surface']['default']['hex']};
                font-family: "Google Sans";
                font-size: 16px;
                padding: 14px;
            }}
            .app-card {{
                background: rgba(0, 0, 0, 0.5);
                border: none;
                border-radius: 24px;
                padding: 28px 24px;
            }}
            .app-card:hover {{
                background: {c['primary_container']['default']['hex']};
            }}
            .app-name {{
                color: {c['on_surface']['default']['hex']};
                font-family: "Google Sans";
                font-size: 14px;
                font-weight: 500;
            }}
        """.encode()
        
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def load_apps(self):
        apps = []
        app_dirs = ["/usr/share/applications", "/var/lib/flatpak/exports/share/applications", 
                    f"{os.path.expanduser('~')}/.local/share/applications",
                    f"{os.path.expanduser('~')}/.local/share/flatpak/exports/share/applications"]
        
        for app_dir in app_dirs:
            if not os.path.exists(app_dir):
                continue
            for file in os.listdir(app_dir):
                if file.endswith(".desktop"):
                    try:
                        app = Gio.DesktopAppInfo.new(file)
                        if app and not app.get_nodisplay():
                            apps.append(app)
                    except:
                        pass
        return apps
    
    def update_apps(self, search=""):
        self.flow.foreach(lambda child: self.flow.remove(child))
        
        search_lower = search.lower() if search else ""
        
        for app in self.apps:
            name = app.get_display_name()
            
            if search_lower and search_lower not in name.lower():
                continue
            
            if self.current_category != "all":
                categories = app.get_categories() or ""
                if self.current_category not in categories:
                    continue
            
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
            box.set_halign(Gtk.Align.CENTER)
            
            icon = Gtk.Image.new_from_gicon(app.get_icon(), Gtk.IconSize.DIALOG)
            icon.set_pixel_size(64)
            box.pack_start(icon, False, False, 0)
            
            label = Gtk.Label(label=name)
            label.get_style_context().add_class("app-name")
            label.set_line_wrap(True)
            label.set_max_width_chars(18)
            label.set_justify(Gtk.Justification.CENTER)
            box.pack_start(label, False, False, 0)
            
            btn = Gtk.Button()
            btn.add(box)
            btn.get_style_context().add_class("app-card")
            btn.connect("clicked", self.on_app_clicked, app)
            btn.app_info = app  # Store for flow activation
            
            self.flow.add(btn)
        
        self.flow.show_all()
    
    def on_category_clicked(self, button, cat):
        for btn in self.category_buttons:
            btn.get_style_context().remove_class("active")
        button.get_style_context().add_class("active")
        
        self.current_category = cat
        self.update_apps(self.search_entry.get_text())
    
    def on_search_changed(self, entry):
        self.update_apps(entry.get_text())
    
    def on_app_clicked(self, button, app):
        app.launch([], None)
        Gtk.main_quit()
    
    def on_flow_activated(self, flowbox, child):
        # Get the button from the child
        btn = child.get_child()
        if btn and hasattr(btn, 'app_info'):
            btn.app_info.launch([], None)
            Gtk.main_quit()
    
    def on_key_press(self, widget, event):
        # ESC to close
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()
            return True
        # Enter to launch selected app
        elif event.keyval in (Gdk.KEY_Return, Gdk.KEY_KP_Enter):
            selected = self.flow.get_selected_children()
            if selected:
                child = selected[0]
                btn = child.get_child()
                if btn and hasattr(btn, 'app_info'):
                    btn.app_info.launch([], None)
                    Gtk.main_quit()
            return True
        # Arrow keys for navigation
        elif event.keyval in (Gdk.KEY_Down, Gdk.KEY_Up, Gdk.KEY_Left, Gdk.KEY_Right):
            if not self.flow.has_focus():
                self.flow.grab_focus()
            return False
        # Any other key focuses search
        elif not self.search_entry.has_focus():
            self.search_entry.grab_focus()
            return False
        return False

win = AppLauncher()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
