import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pathlib import Path
import os

# ============== DATA HANDLER FUNCTIONS ==============

# Use absolute path to ensure file is always found
DATA_FILE = Path(os.path.dirname(os.path.abspath(__file__))) / "todos.json"

def load_todos():
    """Load todos from JSON file."""
    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        else:
            # Create empty file if it doesn't exist
            save_todos([])
            return []
    except (json.JSONDecodeError, Exception) as e:
        st.error(f"Error loading todos: {e}")
        return []

def save_todos(todos):
    """Save todos to JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(todos, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Error saving todos: {e}")
        return False

def get_next_id(todos):
    """Get next unique ID for new todo."""
    if not todos:
        return 1
    return max(t.get("id", 0) for t in todos) + 1

# ============== TODO INPUT COMPONENT ==============

def render_todo_input():
    """Render the to-do input form."""
    st.header("Create a New To-Do")
    
    with st.form("todo_form", clear_on_submit=True):
        todo_title = st.text_input("📌 To-Do Title", placeholder="Enter a task...")
        
        col1, col2 = st.columns(2)
        with col1:
            todo_priority = st.selectbox("⚡ Priority", ["Low", "Medium", "High"])
        with col2:
            todo_category = st.text_input("🏷️ Category", placeholder="e.g., Work, Personal...")
        
        submitted = st.form_submit_button("➕ Add To-Do", use_container_width=True)
        
        if submitted:
            if todo_title.strip():
                todos = load_todos()
                new_todo = {
                    "id": get_next_id(todos),
                    "title": todo_title.strip(),
                    "priority": todo_priority,
                    "category": todo_category.strip(),
                    "completed": False
                }
                todos.append(new_todo)
                if save_todos(todos):
                    st.success("✅ To-Do added successfully!")
                    st.rerun()
            else:
                st.error("❌ Please enter a to-do title!")

# ============== TODO DISPLAY COMPONENT ==============

def render_todo_display():
    """Render active to-do display and management interface."""
    st.header("Active To-Dos")
    
    todos = load_todos()
    active_todos = [t for t in todos if not t.get("completed", False)]
    
    if not active_todos:
        st.info("🎉 No active to-dos! You're all caught up!")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        categories = list(set([t.get("category", "") for t in active_todos if t.get("category")]))
        filter_category = st.multiselect("🏷️ Filter by Category", categories, key="active_cat")
    with col2:
        filter_priority = st.multiselect("⚡ Filter by Priority", ["Low", "Medium", "High"], key="active_pri")
    
    filtered_todos = active_todos
    if filter_category:
        filtered_todos = [t for t in filtered_todos if t.get("category") in filter_category]
    if filter_priority:
        filtered_todos = [t for t in filtered_todos if t.get("priority") in filter_priority]
    
    for todo in filtered_todos:
        priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        priority_color = {"High": "priority-high", "Medium": "priority-medium", "Low": "priority-low"}
        
        priority = todo.get("priority", "Low")
        
        col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
        
        with col1:
            st.markdown(f"""
                <div class="todo-card">
                    <strong>{todo.get('title', 'Untitled')}</strong><br>
                    <small>Category: {todo.get('category') or 'Uncategorized'} | 
                    <span class="{priority_color.get(priority, 'priority-low')}">{priority_emoji.get(priority, '🟢')} {priority}</span></small>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("✓", key=f"complete_{todo['id']}", help="Mark as complete"):
                for t in todos:
                    if t["id"] == todo["id"]:
                        t["completed"] = True
                        break
                save_todos(todos)
                st.rerun()
        
        with col3:
            if st.button("✏️", key=f"edit_{todo['id']}", help="Edit"):
                st.session_state[f"editing_{todo['id']}"] = True
                st.rerun()
        
        with col4:
            if st.button("🗑️", key=f"delete_{todo['id']}", help="Delete"):
                todos = [t for t in todos if t["id"] != todo["id"]]
                save_todos(todos)
                st.rerun()
        
        # Edit form
        if st.session_state.get(f"editing_{todo['id']}", False):
            with st.form(key=f"edit_form_{todo['id']}"):
                new_title = st.text_input("New Title", value=todo.get("title", ""))
                new_category = st.text_input("New Category", value=todo.get("category", ""))
                new_priority = st.selectbox("New Priority", ["Low", "Medium", "High"], 
                                           index=["Low", "Medium", "High"].index(todo.get("priority", "Low")))
                
                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.form_submit_button("💾 Save"):
                        for t in todos:
                            if t["id"] == todo["id"]:
                                t["title"] = new_title.strip()
                                t["category"] = new_category.strip()
                                t["priority"] = new_priority
                                break
                        save_todos(todos)
                        st.session_state[f"editing_{todo['id']}"] = False
                        st.rerun()
                with col_cancel:
                    if st.form_submit_button("❌ Cancel"):
                        st.session_state[f"editing_{todo['id']}"] = False
                        st.rerun()
    
    st.caption(f"📌 Showing {len(filtered_todos)} of {len(active_todos)} active to-dos")

# ============== COMPLETED TODOS COMPONENT ==============

def render_completed_todos():
    """Render completed to-dos display."""
    st.header("Completed To-Dos")
    
    todos = load_todos()
    completed_todos = [t for t in todos if t.get("completed", False)]
    
    if not completed_todos:
        st.info("📭 No completed to-dos yet. Start completing some tasks!")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        categories = list(set([t.get("category", "") for t in completed_todos if t.get("category")]))
        filter_category = st.multiselect("🏷️ Filter by Category", categories, key="completed_cat")
    with col2:
        filter_priority = st.multiselect("⚡ Filter by Priority", ["Low", "Medium", "High"], key="completed_pri")
    
    filtered_todos = completed_todos
    if filter_category:
        filtered_todos = [t for t in filtered_todos if t.get("category") in filter_category]
    if filter_priority:
        filtered_todos = [t for t in filtered_todos if t.get("priority") in filter_priority]
    
    # Clear all completed button
    if st.button("🗑️ Clear All Completed", type="secondary"):
        todos = [t for t in todos if not t.get("completed", False)]
        save_todos(todos)
        st.rerun()
    
    for todo in filtered_todos:
        priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        priority_color = {"High": "priority-high", "Medium": "priority-medium", "Low": "priority-low"}
        
        priority = todo.get("priority", "Low")
        
        col1, col2, col3 = st.columns([4, 1, 1])
        
        with col1:
            st.markdown(f"""
                <div class="todo-card todo-completed">
                    <s><strong>{todo.get('title', 'Untitled')}</strong></s><br>
                    <small>Category: {todo.get('category') or 'Uncategorized'} | 
                    <span class="{priority_color.get(priority, 'priority-low')}">{priority_emoji.get(priority, '🟢')} {priority}</span></small>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("↩️", key=f"undo_{todo['id']}", help="Mark as incomplete"):
                for t in todos:
                    if t["id"] == todo["id"]:
                        t["completed"] = False
                        break
                save_todos(todos)
                st.rerun()
        
        with col3:
            if st.button("🗑️", key=f"delete_completed_{todo['id']}", help="Delete"):
                todos = [t for t in todos if t["id"] != todo["id"]]
                save_todos(todos)
                st.rerun()
    
    st.caption(f"✅ {len(filtered_todos)} completed to-dos")

# ============== ANALYTICS COMPONENT ==============

def render_analytics():
    """Render analytics and visualizations."""
    st.header("To-Do Analytics")
    
    todos = load_todos()
    
    if not todos:
        st.info("No to-dos to analyze yet!")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total To-Dos", len(todos))
    with col2:
        completed = len([t for t in todos if t.get("completed", False)])
        st.metric("Completed", completed)
    with col3:
        st.metric("Remaining", len(todos) - completed)
    with col4:
        if len(todos) > 0:
            completion_rate = round((completed / len(todos)) * 100, 1)
            st.metric("Completion Rate", f"{completion_rate}%")
    
    st.divider()
    
    st.subheader("Priority Distribution")
    priority_data = pd.DataFrame({
        "Priority": [t.get("priority", "Low") for t in todos],
    })
    priority_counts = priority_data["Priority"].value_counts().reset_index()
    priority_counts.columns = ["Priority", "Count"]
    
    fig_priority = px.bar(priority_counts, x="Priority", y="Count", title="To-Dos by Priority",
                          color="Priority", color_discrete_map={"High": "#D32F2F", "Medium": "#F57C00", "Low": "#388E3C"})
    st.plotly_chart(fig_priority, use_container_width=True)
    
    st.subheader("Category Distribution")
    categories = [t.get("category", "Uncategorized") or "Uncategorized" for t in todos]
    if categories:
        category_counts = pd.Series(categories).value_counts().reset_index()
        category_counts.columns = ["Category", "Count"]
        fig_category = px.pie(category_counts, values="Count", names="Category", title="To-Dos by Category")
        st.plotly_chart(fig_category, use_container_width=True)
    
    # Completion status chart
    st.subheader("Completion Status")
    status_data = pd.DataFrame({
        "Status": ["Completed" if t.get("completed") else "Active" for t in todos]
    })
    status_counts = status_data["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    fig_status = px.pie(status_counts, values="Count", names="Status", title="Completion Status",
                        color="Status", color_discrete_map={"Completed": "#4CAF50", "Active": "#2E86AB"})
    st.plotly_chart(fig_status, use_container_width=True)

# ============== MAIN APP ==============

st.set_page_config(page_title="To-Do List", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
        .main-title {
            text-align: center;
            color: #2E86AB;
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .todo-card {
            background-color: #F0F4F8;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #2E86AB;
            margin: 10px 0;
        }
        .todo-completed {
            background-color: #E8F5E9;
            border-left-color: #4CAF50;
        }
        .priority-high {
            color: #D32F2F;
            font-weight: bold;
        }
        .priority-medium {
            color: #F57C00;
            font-weight: bold;
        }
        .priority-low {
            color: #388E3C;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📝 To-Do List Application</div>', unsafe_allow_html=True)

# Show data file location in sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    st.caption(f"📁 Data saved to: `{DATA_FILE}`")
    
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    st.divider()
    
    # Export/Import
    todos = load_todos()
    if todos:
        st.download_button(
            label="📥 Export Todos (JSON)",
            data=json.dumps(todos, indent=2),
            file_name="todos_backup.json",
            mime="application/json"
        )

tab1, tab2, tab3, tab4 = st.tabs(["➕ Add To-Do", "📋 Active To-Dos", "✅ Completed To-Dos", "📊 Analytics"])

with tab1:
    render_todo_input()

with tab2:
    render_todo_display()

with tab3:
    render_completed_todos()

with tab4:
    render_analytics()