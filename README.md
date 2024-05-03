# 장르 별 영화 추천 사이트 구현
-  개요
> -  AJAX와 JSON 데이터를 활용하는 커뮤니티 웹 서비스의 구성
> -  장르 별 영화 데이터 조회가 가능한 애플리케이션
> -  영화 리뷰의 좋아요가 가능한 애플리케이션
> -  유저 간 팔로우가 가능한 애플리케이션
> -  (추가 예정 사항)
>     -  알고리즘을 통한 영화 추천이 가능한 애플리케이션


## 프로젝트 목표
> 데이터를 생성, 조회, 수정, 삭제할 수 있는 애플리케이션 제작
> AJAX와 JSON에 대한 이해
> Many to One relationship(N:1)에 대한 이해
> Many to Many relationship(N:M)에 대한 이해


## 기술 스택
- Python
- Django
- JavaScript

## 기능 목록
### accounts
#### 회원 생성
#### 로그인 및 로그아웃
#### 유저 프로필 조회 및 팔로우
- 유저 팔로우 기능
  ```py
  # accounts/views.py
  @login_required
  def follow(request, user_pk):
      User = get_user_model()
      you = User.objects.get(pk=user_pk)
      me = request.user
      if me != you:
          if me in you.followers.all():
              you.followers.remove(me)
          else:
              you.followers.add(me)
    return redirect('accounts:profile', you.username)
  ```
  - `User = get_user_model()`을 통해 유저 모델 받아오기.
  - you: 요청 받은 user_pk로 조회
  - me: request를 보낸 유저로 조회하여 비교
  
    => 팔로우 되어있지 않다면 팔로우, 팔로우 되어있다면 언팔로우 기능 수행
  - profile 페이지로 redirect



---
### community
#### 전체 리뷰 목록 페이지 조회
#### 새로운 리뷰 생성
#### 단일 댓글 생성
#### 단일 리뷰 상세 페이지 조회 및 좋아요 기능
  ```py
  # community/views.py
  @login_required
  def like(request, review_pk):
      review = Review.objects.get(pk=review_pk)
      me = request.user
      if me in review.like_users.all():
         review.like_users.remove(me)
      else:
          review.like_users.add(me)
      return redirect('community:index')
  ```
  - `review = Review.objects.get(pk=review_pk)`를 통해 리뷰 작성자 조회
  - me: request를 보낸 유저로 조회하여 비교
  
    => 이미 좋아요 되어있다면 좋아요 취소, 그렇지 않으면 좋아요 기능 수행
  - community의 index 페이지로 redirect

---
### movies
#### 전체 영화 목록 페이지 조회
  ```html
  <!-- movies/index.html -->

  <div id="movie-list">
    {% for movie in movies %}
    <div class="movie_box">
      <img src="{{movie.poster_path}}" alt="응애"></img>
      <div class="movie_about">
        <p class="title">{{ movie.title }}</p>
        <div class="movie_info">
          <p><span>개봉일 | </span> {{ movie.release_date }}</p>
          <p><span>인기도 | </span> {{ movie.popularity }}</p>
          <p><span>투표수 | </span>{{ movie.vote_count }}</p>
          <p><span>별점 | </span>{{ movie.vote_average }}</p>
        </div>
        <p class="overview"><span>줄거리 | </span>{% if movie.overview %}
          {{ movie.overview }} {% else %} 줄거리 정보가 없습니다. {% endif %}</p>

      </div>
      <hr>
    </div>
    {% endfor %}
  </div>
  ```
  - index.html로 첫 요청이 왔을 때, 전체 영화 리스트 표시
  - 문자열 형태로 저장된 img_path를 img src=""에 할당하여 이미지 받아오기
  - 줄거리 정보가 없는 영화의 경우 '줄거리 정보가 없습니다'를 출력하도록 DTL 활용 조건분기
#### 필터링 된 영화 데이터 제공
  ```html
  <!-- movies/index.html -->

  <form id="genre-form">
    <select id="genre" name="genre">
      <option value="">장르를 선택하시오.</option>
      {% for genre in genres %}
        <option value="{{ genre.id }}">{{ genre.name }}</option>
      {% endfor %}
    </select>
  </form>
  ```
  - db 내에 장르들을 선택할 수 있도록 select 태그, option 생성, DTL 활용
  ```javascript
  // movies/index.html

  const formTag = document.querySelector('#genre-form');
  const movieList = document.querySelector('#movie-list');

  formTag.addEventListener('change', function(event) {
    event.preventDefault()
    let selectedGenre = event.target.value
    
    axios({
      method: 'get',
      url: "{% url 'movies:filter_genre'%}",
      params: { genre_id: selectedGenre },
    })
    .then((res) => {
      const movies = res.data;
      updateMovieList(movies);
    })  
    .catch((error) => {
      console.log(error)
    })
  })
  ```
  ```py
  # movies/views.py

  def filter_genre(request):
      genre_id = request.GET.get('genre_id')
      if genre_id:
          movies = Movie.objects.filter(genres__id=genre_id).values('id', 'title', 'overview', 'release_date', 'popularity', 'vote_count', 'vote_average', 'poster_path')
      else:
          movies = Movie.objects.all().values('id', 'title', 'overview', 'release_date', 'popularity', 'vote_count', 'vote_average', 'poster_path')

      return JsonResponse(list(movies), safe=False)
  ```
  - select Tag 선택 장르가 변경될 때마다, 선택한 장르 id로 axios 요청
  - 받아온 영화 리스트로 `updateMovieList` callback 함수 실행
  ```javascript
  // movies/index.html

  const formTag = document.querySelector('#genre-form');
  const movieList = document.querySelector('#movie-list');

  formTag.addEventListener('change', function(event) {
    event.preventDefault()
    let selectedGenre = event.target.value
    
    axios({
      method: 'get',
      url: "{% url 'movies:filter_genre'%}",
      params: { genre_id: selectedGenre },
    })
    .then((res) => {
      const movies = res.data;
      updateMovieList(movies);
    })
    .catch((error) => {
      console.log(error)
    })
  })

  function updateMovieList(movies) {
    movieList.innerHTML = '';

    movies.forEach(movie => {
      const movieElement = document.createElement('div') 

      movieElement.innerHTML = `
      <div class="movie_box">
        <img src="${movie.poster_path}" alt="${movie.title}">
        <div class="movie_about">
          <p class="title">${movie.title}</p>
          <div class="movie_info">
            <p><span>개봉일 | </span> ${movie.release_date}</p>
            <p><span>인기도 | </span>${movie.popularity}</p>
            <p><span>투표수 | </span>${movie.vote_count}</p>
            <p><span>별점 | </span>${movie.vote_average}</p>
          </div>
          <p class="overview"><span>줄거리 | </span>${movie.overview ? movie.overview : '줄거리 정보가 없습니다.'}</p>
        </div>
        <hr>
      </div>
      `;
      movieList.appendChild(movieElement)
    })
  }
  ```
  - 기존에 있던 영화 목록 초기화 및 받아온 영화 데이터로 갱신
#### 영화 추천 페이지 조회 (미완성)
---
### 각 페이지 별 css 적용
`/assets/style/*.css`
- base
  - navbar 구조 및 계정 관련 기능들 우측 정렬
- community_index
  - 디자인 및 id, 작성자, 내용 정렬
  - 좋아요 관련 요소 우측 정렬
- create
  - 새 글 만들기 form UI/UX 정리 및 통일
  - 돌아가기 버튼 및 게시 버튼
- detail
  - 리뷰 작성 시간 및 수정 시각 분리 표시
  - 영화 제목, 평점, 내용 디자인
  - 댓글 목록 디자인
  - 작성자의 이름이 댓글 입력 칸 옆에 표시되도록 설정
- login
  - 로그인 폼 디자인 수정
- movie_index
  - 전체 디자인 및 장르 선택 tag 디자인
  - 개봉일, 인기도, 투표수, 별점, 줄거리 정렬
  - 줄거리가 너무 긴 영화는 3줄까지만 표시되도록 정리
- profile
  - 전체 디자인
---
## 어려웠던 부분
- 전체 프로젝트의 디자인을 직접 구상하고, 통일성을 갖도록 꾸미기
- Django가 기본 제공하는 form을 분해하여 각 요소별로 꾸미기
- javascript로만 반응형 변수들을 업데이트 하는 것
- API 요청 및 자료 분석, 데이터의 요소 별로 영화 추천 알고리즘 구상
## 해결 방안
- Chrome의 개발자 도구를 통해 각 요소 별로 class, style을 하나 씩 확인하며 점차적으로 진행
  - 개발자 도구를 통해 기본 form이 갖는 요소들을 분해할 수 있었음.
- 반응형 업데이트를 위해 원래 있던 데이터를 초기화하고, 새로 업데이트
- 알고리즘 구상은 추후 업데이트 예정