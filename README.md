[![codecov](https://codecov.io/gh/yuki0417/travel-app/branch/master/graph/badge.svg)](https://codecov.io/gh/yuki0417/travel-app)

# 周辺情報検索アプリ

## サービスの概要
手軽に周辺のスポットを検索して、お散歩ができるサービスです。
#### https://travel.mytravelapp.net/

### 主な機能

- MediaWiki APIの検索設定
- MediaWiki APIを利用して位置情報をもとに周りのスポットを検索
- 簡易逆ジオコーディングサービスを利用して緯度経度情報から住所情報を取得
- 気になったスポットの保存
- 気になったスポットへの経路案内
- 保存したスポットへのコメント、シェア機能
- シェアされているスポットの一覧

## 開発環境
VirtualBoxとVagrantでCentOS7の仮想マシンを構築し、そのマシンで作成したDockerコンテナを使用。
<br>
※利用したVagrantfileはソースに含めていない。

## 開発言語とフレームワーク
- Python、Django
- JavaScript、jQuery、Bootstrap

## インフラ
- 本番環境
    - ECS、Fargate、ECR、RDS、ElastiCache、S3、ALB、Route53
- 検証環境
    - EC2に、使用するミドルウェア（Django、Nginx、PostgreSQL、Redis）をDockerで構築

![system_architecture.png](https://github.com/yuki0417/travel-app/blob/master/system_architecture.png?raw=true)

## コード管理ツール
- GitHub

## CI/CDツール
- CircleCI
- Codecov

## 使用しているミドルウェア

### リバースプロキシ
- Nginx

### データベース
- PostgreSQL

### セッション管理
- Redis

### その他のミドルウェア
- 本番環境
    - requirements.txt を参照。
- 開発環境
    - requirements_dev.txt を参照。

## テストツール
- 単体テスト
    - Django標準のユニットテスト機能
- 統合テスト
    - Selenium (Chromeドライバを使用)

html形式のテストレポートとカバレッジレポートがCircleCI上で確認可能。

## 使用しているAPIサービス
- [MediaWiki API](https://www.mediawiki.org/wiki/API:Main_page)
- [簡易逆ジオコーディングサービス（農研機構）](https://www.finds.jp/rgeocode/index.html)

## 心がけたこと
- 本番環境と開発環境の差異をDockerコンテナ技術により少なくする
- インフラのコード化
- 機能拡張を意識したコーディング、テスト実装
- レスポンシブデザイン
- ログインシステム、ユーザーモデルを完全に自作
