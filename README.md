# ESuits

![IMAGE ALT TEXT HERE](static/esuits/images/logo.png)

## 製品概要
エントリーシート X Tech


### 背景(製品開発のきっかけ、課題等）
私達のチームは同じ研究室に所属する同級生です．就活の時期がやってきて，皆が真っ先に直面した問題はエントリーシート (ES) を書く難しさです．ES作成は就活生にとって永遠の悩みでしょう．前にも似たようなことを書いたけど，どこにメモしたか忘れてしまった．そもそも何を書いていいのかわからない．そんな問題に一度は直面したことがあるのではないでしょうか？　このアプリケーションはそんな就活生の悩みを解決できます．今まで自分が書いたESをこのサービスで溜めていけば，効率よく自分の回答を探すことができます．さらにESを編集する画面では，志望企業に合格する近道となるキーワードを見たり，その業界に関するニュースをゲットできたりします．就活生の生活を明るく楽しいものにしようと考え，このアプリケーションを開発しました．


### 製品説明（具体的な製品の説明）

### esuits 利用の流れ
1. サービスにログインします．

![IMAGE ALT TEXT HERE](screenshots/login.png)

2. 次に表示されるのはホーム画面です．ここに今まで作成したESが表示されます．

![IMAGE ALT TEXT HERE](screenshots/home.png)

3. 「新規作成」ボタンを押して新しいESの情報を登録します．志望企業の名前やURL，質問を入力します．質問にはジャンルによって「ガクチカ」「志望動機」などのタグを付けられます．

![IMAGE ALT TEXT HERE](screenshots/create.png)

4. エントリーシートの回答を作成します．画面右側には志望企業のウェブサイトから生成したワードクラウド・その企業に関するニュースが表示されます．さらに各回答フォームの下には過去に作成した類似の回答を表示できます．これらの情報を参考にして，効率よくESを完成させましょう．

![IMAGE ALT TEXT HERE](screenshots/edit.png)


### 特長
1. 特長1
過去に自分が書いた回答を参考にして効率よくESを作ろう！

2. 特長2
志望企業に関するニュースを見て，業界のトレンドや時事問題に詳しくなれる！

3. 特長3
志望企業のウェブサイトから生成したワードクラウドを見て，エントリーシートに含めたいキーワードが一目でわかる！


### 解決出来ること
1. 自分が今まで書いたESを保管することができる．
2. 回答にタグをつけて整理できる．
3. 過去に自分が書いた文章を参考にして効率よくエントリーシートを作成できる．
4. 就活生が志望企業や志望業界のトレンドを知ることができる．


### 今後の展望

今回はデプロイ先でワードクラウドの画像がうまく表示されない問題が起きてしまったが，
サービスとして実用的なアプリケーションになるように開発を続けたいと思っています．

### 注力したこと（こだわり等）
* チーム内での役割分担
* フロントエンドのデザインの統一．
* データベースの設計．特にESの質問・回答にタグをつけるためにMany-to-Manyのフィールドを使用した．
* ワードクラウドの生成など，時間がかかる処理はajaxで非同期処理を使った．

## 開発技術
### 活用した技術
#### API・データ
* Google News API

#### フレームワーク・ライブラリ・モジュール
* Django
* jQuery
* BootStrap
* Word Cloud


### 独自技術
#### ハッカソンで開発した独自機能・技術
* 志望企業の採用サイトからクロールしたテキストに自然言語処理を行い，ワードクラウドを生成．


#### 製品に取り入れた研究内容（データ・ソフトウェアなど）（※アカデミック部門の場合のみ提出必須）
*
*
