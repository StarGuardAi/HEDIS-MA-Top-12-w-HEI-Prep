// Project database for filtering and search
const projects = [
    {
        id: 1,
        title: "HEDIS Star Rating Crisis Prevention",
        category: "AI/ML",
        impact: "$150-200M Crisis Prevention Value",
        description: "AI system that predicts HEDIS measure gaps 6-12 months early across 12 quality measures, preventing catastrophic Star Rating drops for Medicare Advantage plans.",
        tags: ["Python", "Scikit-learn", "FastAPI", "HIPAA", "Healthcare", "Machine Learning"],
        skills: ["Machine Learning", "Python", "Healthcare", "API Development"],
        liveDemo: "https://hedis-ma-top-12-w-hei-prep.streamlit.app/",
        code: "https://github.com/bobareichert/HEDIS-MA-Top-12-w-HEI-Prep",
        caseStudy: "featured/hedis-star-rating-system/",
        featured: true,
        metrics: {
            accuracy: "91%",
            value: "$13M-$27M",
            roi: "196%"
        }
    },
    {
        id: 2,
        title: "Enterprise SQL Data Integration",
        category: "Data Engineering",
        impact: "$200M+ Documented Savings",
        description: "Designed SQL Server data marts that integrated claims, clinical, and pharmacy data, enhancing healthcare program performance by 34% and reducing readmissions by 40%.",
        tags: ["SQL Server", "ETL", "Healthcare Coding", "Data Quality"],
        skills: ["SQL", "ETL", "Healthcare", "Data Quality"],
        caseStudy: "featured/sql-data-integration/",
        featured: true,
        metrics: {
            savings: "$200M+",
            improvement: "34%",
            reduction: "40%"
        }
    },
    {
        id: 3,
        title: "Executive Dashboard Suite",
        category: "Business Intelligence",
        impact: "22% Satisfaction Gain | $32M Bonuses",
        description: "Built Tableau and Power BI dashboards that increased CMS member satisfaction by 22%, supported $32M in performance bonuses, and saved 14 hours/week in reporting.",
        tags: ["Tableau", "Power BI", "Plotly", "Real-time Analytics"],
        skills: ["Tableau", "Power BI", "Data Visualization", "Healthcare"],
        liveDemo: "https://hedis-ma-top-12-w-hei-prep.streamlit.app/",
        caseStudy: "featured/dashboard-suite/",
        featured: true,
        metrics: {
            satisfaction: "+22%",
            bonuses: "$32M",
            timeSaved: "14 hrs/week"
        }
    }
];

// Unique skill tags for filtering
const allSkills = [
    "Machine Learning",
    "Python",
    "Healthcare",
    "SQL",
    "Tableau",
    "Power BI",
    "FastAPI",
    "ETL",
    "Data Visualization",
    "API Development",
    "HIPAA Compliance",
    "Data Quality"
];

// Filter projects by skill
function filterProjectsBySkill(skill) {
    if (skill === 'all') {
        return projects;
    }
    return projects.filter(project => project.skills.includes(skill));
}

// Search projects by keyword
function searchProjects(query) {
    const lowerQuery = query.toLowerCase();
    return projects.filter(project => 
        project.title.toLowerCase().includes(lowerQuery) ||
        project.description.toLowerCase().includes(lowerQuery) ||
        project.tags.some(tag => tag.toLowerCase().includes(lowerQuery))
    );
}

// Filter by category
function filterByCategory(category) {
    if (category === 'all') {
        return projects;
    }
    return projects.filter(project => project.category === category);
}

// Render project card
function renderProjectCard(project) {
    const card = document.createElement('div');
    card.className = 'project-card';
    card.dataset.skills = JSON.stringify(project.skills);
    card.dataset.category = project.category;
    
    const metricsHTML = Object.entries(project.metrics || {})
        .map(([key, value]) => `<span class="tag">${value}</span>`)
        .join('');
    
    const linksHTML = `
        ${project.liveDemo ? `<a href="${project.liveDemo}" target="_blank" class="project-link">🌐 Live Demo</a>` : ''}
        ${project.code ? `<a href="${project.code}" target="_blank" class="project-link secondary">💻 Code</a>` : ''}
        ${project.caseStudy ? `<a href="${project.caseStudy}" class="project-link secondary">📄 Case Study</a>` : ''}
    `;
    
    const tagsHTML = project.tags.map(tag => `<span class="tag">${tag}</span>`).join('');
    
    card.innerHTML = `
        <div class="project-header">
            <h3 class="project-title">${project.title}</h3>
            <p class="project-impact">${project.impact}</p>
        </div>
        <div class="project-body">
            <p class="project-description">${project.description}</p>
            <div class="project-tags">
                ${metricsHTML}
            </div>
            <div class="project-tags">
                ${tagsHTML}
            </div>
            <div class="project-links">
                ${linksHTML}
            </div>
        </div>
    `;
    
    return card;
}

// Initialize filters
function initializeFilters() {
    const filterContainer = document.getElementById('skill-filters');
    if (!filterContainer) return;
    
    // Add "All" filter
    const allButton = document.createElement('button');
    allButton.className = 'filter-button active';
    allButton.textContent = 'All Projects';
    allButton.onclick = () => {
        document.querySelectorAll('.filter-button').forEach(btn => btn.classList.remove('active'));
        allButton.classList.add('active');
        renderAllProjects(projects);
    };
    filterContainer.appendChild(allButton);
    
    // Add skill filters
    allSkills.forEach(skill => {
        const button = document.createElement('button');
        button.className = 'filter-button';
        button.textContent = skill;
        button.onclick = () => {
            document.querySelectorAll('.filter-button').forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            const filtered = filterProjectsBySkill(skill);
            renderAllProjects(filtered);
        };
        filterContainer.appendChild(button);
    });
}

// Render all projects
function renderAllProjects(projectList = projects) {
    const container = document.getElementById('projects-grid');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (projectList.length === 0) {
        container.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--text-light);">No projects match your filter.</p>';
        return;
    }
    
    projectList.forEach(project => {
        container.appendChild(renderProjectCard(project));
    });
}

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById('project-search');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value;
        const results = searchProjects(query);
        renderAllProjects(results);
    });
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        initializeFilters();
        initializeSearch();
        renderAllProjects();
    });
} else {
    initializeFilters();
    initializeSearch();
    renderAllProjects();
}

// Export for external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { projects, filterProjectsBySkill, searchProjects, allSkills };
}

