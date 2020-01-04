## 開発環境
Vagrant上のCentOS7に作成したDockerコンテナを使用。

## 開発言語とフレームワーク
- PythonのDjangoフレームワーク
- JavaScript、jQuery、Bootstrap

## インフラ
- 本番環境
- - ECS、ECR、RDS、ElastiCache、S3、ALB
- 検証環境
- - EC2に、使用するミドルウェア（Django、Nginx、PostgreSQL、Redis）をDockerで構築

詳細はリポジトリの system_architecture.png を参照。

## コード管理ツール
- GitHub

## CI/CDツール
- CircleCI

## リバースプロキシ
- Nginx

## データベース
- PostgreSQL

## セッション管理
- Redis

## テストツール
- 単体テスト
- - Django標準のユニットテスト機能
- 統合テスト
- - Selenium (Chromeドライバを使用)

## その他ミドルウェア
- 本番環境
requirements.txt を参照。
- 開発環境
requirements_dev.txt を参照。

## 心がけたこと
- 本番環境と開発環境の差異をDockerコンテナ技術により少なくする
- インフラのコード化
- 機能拡張を意識したコーディング、テスト実装
- Gitのブランチの使い分け、コミット単位の調整、プルリクエストの活用