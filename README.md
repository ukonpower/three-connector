# Three Connector
Blender上でのアニメーションやタイムラインをリアルタイムに同期するためのBlenderアドオンです。

# Install

1. websocketsをインストール  
	Blenderとブラウザ間の同期にはWebsocketを利用するため、[websockets](https://websockets.readthedocs.io/)をインストールする必要があります。  
	websocketsの[リポジトリ](https://github.com/aaugustin/websockets)よりソースコードをダウンロードし、`src/websockets`ディレクトリをBlenderのPythonライブラリディレクトリにコピーします。

	例:
	- Windows  
	`` C:/Program Files/Blender Foundation/Blender <version>/<version>/python/lib``

	- Mac  
		``/Applications/Blender.app/Contents/Resources/2.81/python/lib/python<version>``

2. アドオンのインストール  
   ``/three-connect``フォルダをBlenderの``scripts/addons/``フォルダにコピーします。

# Usage
![panel](/screenshots/panel.png)

3Dビューポート > サブメニュー > `ThreeConnector`タブ から操作できます。

## Sync
WebSocketを用いてWebブラウザとシーンの同期をします。  

シーン同期には以下のデータが利用されます。（構造は違います）

- シーンデータ
	|  プロパティ名  |  -  |
	| ---- | ---- |
	|  actions  |  シーンで利用されているアニメーションアクション（のFCurveを抽出したもの）のリスト  |
	|  objects  |  シーンに存在するオブジェクトとそれに対して利用されているアニメーションアクションのリスト  |

- タイムラインデータ
	|  プロパティ名  |  -  |
	| ---- | ---- |
	|  start  |  タイムラインの開始フレーム  |
	|  end  |  タイムラインの終了フレーム  |
	|  current  |  現在のフレーム  |

また、以下のタイミングでデータが送信されます。

1. **WebSocket接続時**  
   クライアント接続時にその時点の`シーンデータ`と`タイムラインデータ`を送信します。
2. **プロジェクト保存時**  
	.blendファイルを保存する際にその時点の`シーンデータ`を送信します。
4. **フレーム変更時**  
	フレームが変更された際に、その時点の`タイムラインデータ`が送信されます。

### ポート
コントロールパネル状の`port`からWebSocketサーバで使用されるポート番号を変更することができます。（デフォルトは3100番)

## glTF Export
シーンのglTFエクスポートのショートカットボタンです。  
`path`と`preset`で指定された設定で出力されます。
## Json Export
WebSocketで送信されるシーンデータをJSONとして出力します。  

## 参考
- クライアント側サンプル  
	https://github.com/ukonpower/ore-three-ts/blob/feature/create-blender_connector/examples/BlenderConnector/src/ts/BlenderConnectorScene.ts

## Next Stage...

- example作れ
- ドキュメントを整備しろ  