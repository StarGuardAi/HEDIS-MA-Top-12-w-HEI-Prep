# Mobile Navigation System Usage Guide

## Overview

Complete mobile navigation system for HEDIS Portfolio Optimizer with state management, deep linking, and smooth transitions.

## Quick Start

```python
import streamlit as st
from utils.mobile_navigation import create_mobile_app_structure

# Define view handlers
def render_dashboard():
    st.write("Dashboard content")

def render_opportunities():
    st.write("Opportunities content")

# Create app structure
view_handlers = {
    'dashboard': render_dashboard,
    'opportunities': render_opportunities
}

create_mobile_app_structure(view_handlers)
```

## Navigation Components

### 1. Navigation Header

**Sticky header with logo and menu button**

```python
from utils.mobile_navigation import create_mobile_nav_header

create_mobile_nav_header(show_menu_button=True)
```

**Features:**
- Sticky positioning (stays at top)
- Logo/Title display
- Last updated timestamp
- Menu button (optional)

### 2. View Selector

**Primary navigation dropdown**

```python
from utils.mobile_navigation import mobile_view_selector

current_view = mobile_view_selector()
```

**Available Views:**
- 📊 Dashboard
- 🎯 Top Opportunities
- 📈 My Measures
- 👥 Members
- ⚙️ Settings

### 3. Hamburger Menu

**Secondary actions and account options**

```python
from utils.mobile_navigation import mobile_hamburger_menu

mobile_hamburger_menu()
```

**Menu Options:**
- 🔄 Refresh
- 📥 Export
- 📧 Share
- ❓ Help
- 🔍 Quick Filters
- ⚙️ Preferences
- 🚪 Sign Out

### 4. Back Button

**Navigate to previous view**

```python
from utils.mobile_navigation import mobile_back_button

mobile_back_button()
```

**Features:**
- Only shows if navigation history exists
- Restores previous view state
- Maintains context (selected items, filters)

### 5. Breadcrumbs

**Show navigation path**

```python
from utils.mobile_navigation import mobile_breadcrumbs

mobile_breadcrumbs()
```

**Displays:**
- Current view path
- Selected measure (if any)
- Selected member (if any)

## State Management

### Initialize State

```python
from utils.mobile_navigation import init_mobile_state

init_mobile_state()
```

**Initializes:**
- Navigation state
- View history
- Selected items
- Filter presets
- UI state (modals, menus)

### Save Navigation State

```python
from utils.mobile_navigation import save_nav_state, get_nav_context

context = get_nav_context()
save_nav_state('dashboard', context)
```

**Saves:**
- Current view
- Selected measure/member
- Filter settings
- Pagination limits

### Navigation History

```python
# Access history
nav_history = st.session_state.nav_history

# Each item contains:
# - view: View identifier
# - context: Saved context dict
# - timestamp: When navigated
```

## Deep Linking

### Handle URL Parameters

```python
from utils.mobile_navigation import handle_mobile_url_params

handle_mobile_url_params()
```

**Supported Parameters:**
- `?view=dashboard` - Set current view
- `?view=measures&measure=HbA1c+Testing` - View with measure selected
- `?view=members&member=M12345678` - View with member selected
- `?preset=executive` - Load filter preset

### Create Shareable Links

```python
from utils.mobile_navigation import create_shareable_mobile_link

url = create_shareable_mobile_link()
st.code(url)
```

**Generated URLs:**
- Include current view
- Include selected measure (if any)
- Include selected member (if any)
- Include filter preset (if not default)

## View Router

### Define View Handlers

```python
def render_dashboard():
    st.markdown("### Dashboard")
    # Your dashboard content

def render_opportunities():
    st.markdown("### Opportunities")
    # Your opportunities content

view_handlers = {
    'dashboard': render_dashboard,
    'opportunities': render_opportunities,
    'measures': render_measures,
    'members': render_members,
    'settings': render_settings
}
```

### Route Views

```python
from utils.mobile_navigation import mobile_router

mobile_router(view_handlers)
```

**Features:**
- Automatic routing based on `current_view`
- Error handling for unknown views
- Fallback to dashboard

## Modal System

### Show Modal

```python
from utils.mobile_navigation import show_mobile_modal

def render_export_content():
    st.write("Export options here")

show_mobile_modal("Export Data", render_export_content, key="export")
```

**Built-in Modals:**
- Export: `render_export_options()`
- Share: `render_share_content()`
- Help: `render_help_content()`

### Custom Modal

```python
def my_custom_content():
    st.write("Custom content")
    if st.button("Action"):
        st.success("Done!")

show_mobile_modal("Custom Modal", my_custom_content, key="custom")
```

## Complete App Structure

### Full Integration

```python
import streamlit as st
from utils.mobile_navigation import create_mobile_app_structure

# Page config
st.set_page_config(
    page_title="HEDIS Mobile",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Define view handlers
def render_dashboard():
    st.write("Dashboard")

def render_opportunities():
    st.write("Opportunities")

# ... other views

view_handlers = {
    'dashboard': render_dashboard,
    'opportunities': render_opportunities,
    'measures': render_measures,
    'members': render_members,
    'settings': render_settings
}

# Create app structure
create_mobile_app_structure(
    view_handlers,
    show_header=True,
    show_back_button=True,
    show_breadcrumbs=True,
    show_menu=True
)
```

## Navigation Patterns

### Pattern 1: Simple Navigation

```python
# Just view selector
current_view = mobile_view_selector()

# Route manually
if current_view == 'dashboard':
    render_dashboard()
elif current_view == 'opportunities':
    render_opportunities()
```

### Pattern 2: Full Navigation System

```python
# Complete system with all features
create_mobile_app_structure(view_handlers)
```

### Pattern 3: Custom Navigation

```python
# Header only
create_mobile_nav_header()

# Custom view selector
# Custom routing
# Custom menu
```

## State Persistence

### Across Navigation

- View state persists
- Selected items persist
- Filter settings persist
- Pagination limits persist

### Across Sessions

- Use URL parameters for deep linking
- Share links preserve state
- Back button restores previous state

## URL Parameters Reference

### View Parameter

```
?view=dashboard
?view=opportunities
?view=measures
?view=members
?view=settings
```

### Measure Parameter

```
?view=measures&measure=HbA1c+Testing
```

### Member Parameter

```
?view=members&member=M12345678
```

### Preset Parameter

```
?preset=executive
?preset=care_coordinator
```

### Combined

```
?view=measures&measure=HbA1c+Testing&preset=financial_focus
```

## Testing Checklist

### Navigation

- [ ] View selector changes views correctly
- [ ] Back button navigates to previous view
- [ ] Breadcrumbs show correct path
- [ ] State persists across navigation

### Deep Linking

- [ ] URL parameters load correct view
- [ ] Selected items load from URL
- [ ] Share links work correctly
- [ ] Parameters are URL-encoded

### Modals

- [ ] Modals open when triggered
- [ ] Modals close correctly
- [ ] Multiple modals don't conflict
- [ ] Modal content renders properly

### State Management

- [ ] State initializes correctly
- [ ] Navigation history maintained
- [ ] Context saved/restored
- [ ] No state conflicts

## Best Practices

### 1. Initialize Early

```python
# At top of app
init_mobile_state()
handle_mobile_url_params()
```

### 2. Save State Before Navigation

```python
context = get_nav_context()
save_nav_state(current_view, context)
```

### 3. Use View Handlers

```python
# ✅ Good: Organized view handlers
view_handlers = {
    'dashboard': render_dashboard,
    'opportunities': render_opportunities
}

# ❌ Bad: Inline routing logic
if view == 'dashboard':
    # ... lots of code
```

### 4. Handle Errors

```python
try:
    mobile_router(view_handlers)
except Exception as e:
    st.error(f"Navigation error: {e}")
    st.session_state.current_view = 'dashboard'
```

## Troubleshooting

### Navigation Not Working

- Check `init_mobile_state()` is called
- Verify view handlers are defined
- Check `current_view` in session state

### State Not Persisting

- Ensure `save_nav_state()` is called
- Check navigation history exists
- Verify context is saved

### URL Parameters Not Loading

- Check `handle_mobile_url_params()` is called
- Verify parameter names match
- Check URL encoding

### Modals Not Showing

- Check `show_*` flags in session state
- Verify modal key is unique
- Check modal content function

## Examples

See `mobile_navigation.py` for complete examples and `mobile_view.py` for integration patterns.

---

## Support

For questions or issues:
- 📧 **Email**: reichert.starguardai@gmail.com
- 🔗 **LinkedIn**: [sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics/)
- 💻 **GitHub**: [HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/blob/main/README.md)
- 🎨 **Portfolio**: [Canva Portfolio](https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit)

---

**Mobile Navigation** | State management | Deep linking | Smooth transitions 📱

