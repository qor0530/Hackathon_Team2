document.addEventListener('DOMContentLoaded', () => {
    const duplicateCheckButton = document.getElementById('duplicate-check');
    const signupForm = document.getElementById('info-form');
    let loginIds = [];
  
    // Fetch all login_ids
    async function fetchLoginIds() {
      try {
        const response = await fetch('/api/user/login_ids');
        loginIds = await response.json();
      } catch (error) {
        console.error('Error fetching login IDs:', error);
      }
    }
  
    // Call fetchLoginIds on page load
    fetchLoginIds();
    
    // 중복 확인 fetch 요청
    duplicateCheckButton.addEventListener('click', (event) => {
      event.preventDefault();
      const idInput = document.getElementById('id-input').value;
      
      if (idInput === '') {
        alert('아이디를 입력해주세요.');
        return;
      }
  
      if (loginIds.includes(idInput)) {
        alert('이미 사용중인 아이디입니다.');
      } else {
        alert('사용 가능한 아이디입니다.');
      }
    });
  
    // 회원 가입 fetch 요청
    signupForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const nickname = document.getElementById('nickname-input').value;
      const password = document.querySelector('.password-input').value;
      const passwordCheck = document.getElementById('password-check').value;
      const idInput = document.getElementById('id-input').value;
      
      if (password !== passwordCheck) {
        alert('비밀번호가 일치하지 않습니다.');
        return;
      }
  
      if (loginIds.includes(idInput)) {
        alert('이미 사용중인 아이디입니다. 다른 아이디를 사용해주세요.');
        return;
      }
      
      try {
        const response = await fetch('/api/user/create', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            login_id: idInput,
            password1: password,
            password2: passwordCheck,
            nickname: nickname,
            profile_image: '',
            learning_history: '',
            total_learning_time: 0,
            level: 1,
            exp: 0,
            ranking_score: 0,
            subscription: false,
            ranking: 0,
            attendance: 0
          })
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
          alert('회원 가입에 성공했습니다.');
          window.location.href = '/test';
        } else {
          alert('회원 가입에 실패했습니다. ' + (result.detail || ''));
        }
      } catch (error) {
        alert('회원 가입에 성공했습니다.');
        window.location.href = '/test';
      }
    });
  });