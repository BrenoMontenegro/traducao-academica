window.addEventListener('scroll', () => {
      const header = document.getElementById('header');
      header.classList.toggle('scrolled', window.scrollY > 20);
    });

    function toggleMobileMenu() {
      console.log('Mobile menu toggled');
    }

    document.querySelectorAll('.nav-link, .action-btn, .user-profile').forEach(element => {
      element.addEventListener('mouseenter', () => element.style.transform = 'translateY(-2px)');
      element.addEventListener('mouseleave', () => element.style.transform = 'translateY(0)');
    });