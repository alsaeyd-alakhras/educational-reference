import os
import re

files = [
    'index.html',
    'courses.html',
    'course.html',
    'blog.html',
    'article.html',
    'stage.html',
    'login.html',
    'register.html'
]

# The original logo block pattern
logo_regex = re.compile(
    r'<a href="[^"]*" class="flex items-center gap-3 shrink-0">\s*<div class="flex flex-col items-end">\s*<span class="font-tajawal font-bold text-\[28px\] leading-tight text-primary-dark">المرجعية التربوية</span>\s*</div>\s*<div class="w-12 h-12 rounded-full overflow-hidden shrink-0">\s*<img src="https://www.figma.com/api/mcp/asset/73f79792-f273-490b-9fad-4ebdf0d9d4dc" alt="المرجعية التربوية"\s*class="w-full h-full object-cover" />\s*</div>\s*</a>',
    re.DOTALL
)

new_logo = """<a href="index.html" class="flex items-center gap-3 shrink-0 group transition-all duration-300 hover:-translate-y-1 page-transition-link">
          <div class="flex flex-col items-end">
            <span class="font-tajawal font-bold text-[28px] leading-tight text-primary-dark group-hover:text-primary transition-colors duration-300">المرجعية التربوية</span>
          </div>
          <div class="w-12 h-12 rounded-full overflow-hidden shrink-0 group-hover:shadow-lg group-hover:scale-110 transition-all duration-300">
            <img src="https://www.figma.com/api/mcp/asset/73f79792-f273-490b-9fad-4ebdf0d9d4dc" alt="المرجعية التربوية"
              class="w-full h-full object-cover" />
          </div>
        </a>"""

script_to_add = """
  <!-- Page Transition Script -->
  <style>
    body {
      opacity: 0;
      transform: translateY(-10px);
      transition: opacity 0.5s ease-out, transform 0.5s ease-out;
    }
    body.page-loaded {
      opacity: 1;
      transform: translateY(0);
    }
    body.page-fade-out {
      opacity: 0;
      transform: translateY(10px);
    }
  </style>
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      // Fade in on load
      setTimeout(() => {
        document.body.classList.add('page-loaded');
      }, 50);

      // Add click listener for smooth page transition
      const transitionLinks = document.querySelectorAll('.page-transition-link');
      transitionLinks.forEach(link => {
        link.addEventListener('click', (e) => {
          const href = link.getAttribute('href');
          const isHome = window.location.pathname.endsWith('index.html') || window.location.pathname.endsWith('/');
          
          if (href === 'index.html' && isHome) {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
            return;
          }

          if (href && href !== '#' && !href.startsWith('#')) {
            e.preventDefault();
            document.body.classList.remove('page-loaded');
            document.body.classList.add('page-fade-out');
            setTimeout(() => {
              window.location.href = href;
            }, 400);
          }
        });
      });
    });
  </script>
"""

for filename in files:
    if not os.path.exists(filename):
        continue
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update logo
    content = logo_regex.sub(new_logo, content)

    # 2. Update 'الرئيسية' link to have page-transition-link class and be an active interactive element
    # In desktop nav:
    content = re.sub(
        r'<a href="[^"]*" class="nav-link (active )?font-readex font-bold text-\[14px\] text-primary pb-1.5">الرئيسية</a>',
        r'<a href="index.html" class="nav-link \1font-readex font-bold text-[14px] text-primary pb-1.5 page-transition-link transform hover:scale-105 transition-all duration-300">الرئيسية</a>',
        content
    )
    content = re.sub(
        r'<a href="[^"]*" class="nav-link font-readex font-medium text-\[14px\] text-\[#414845\] hover:text-primary pb-1.5">الرئيسية</a>',
        r'<a href="index.html" class="nav-link font-readex font-medium text-[14px] text-[#414845] hover:text-primary pb-1.5 page-transition-link transform hover:scale-105 transition-all duration-300">الرئيسية</a>',
        content
    )
    
    # In mobile nav:
    content = re.sub(
        r'<a href="[^"]*" class="font-readex font-bold text-\[14px\] text-primary py-2 border-b border-border/50">الرئيسية</a>',
        r'<a href="index.html" class="font-readex font-bold text-[14px] text-primary py-2 border-b border-border/50 page-transition-link">الرئيسية</a>',
        content
    )
    content = re.sub(
        r'<a href="[^"]*" class="font-readex font-medium text-\[14px\] text-\[#414845\] py-2 border-b border-border/50">الرئيسية</a>',
        r'<a href="index.html" class="font-readex font-medium text-[14px] text-[#414845] py-2 border-b border-border/50 page-transition-link">الرئيسية</a>',
        content
    )

    # 3. Insert script before </body>
    if '<!-- Page Transition Script -->' not in content:
        content = content.replace('</body>', script_to_add + '\n</body>')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done updating animations.")
