# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> Path: tokenB->tokenA->tokenC->tokenE->tokenD->tokenC->tokenB,
> Value: 5       5.655   2.372   1.530   3.450   6.684   22.497
> log:
  After Arbitrage tokenA Balance: 5655321988655321988
  After Arbitrage tokenC Balance: 2372138936383089007
  After Arbitrage tokenE Balance: 1530137136963616993
  After Arbitrage tokenD Balance: 3450741448619708083
  After Arbitrage tokenC Balance: 6684525579572586452
  After Arbitrage tokenB Balance: 22497221806974138089

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> 在AMM(自動做市商)中，滑點指的是實際報酬與預期報酬的落差，之所以會發生這件事情是因為AMM中token的價格由恆定成績公式決定，所有跟你有一樣交易目標的人都有可能害你的交易後得到的token變少(其實就有點類似於供需取線，有人把你想要的商品先一步買走，供給降低售價就會上升)。為了解決這個問題，我們可以為交易設定最大滑點容忍度：

```solidity
  function swapExactTokensForTokens(
    uint amountIn,
    uint amountOutMin,
    address[] calldata path,
    address to,
    uint deadline
  ) external returns (uint[] memory amounts);
```

> 上面的function是Uniswap V2 Router02 中的函式，其中參數amountOutMin就是用來確保最終得到的token部會低於某個值，藉此避免滑點太嚴重。

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> 簡單來說，這個設計是為了讓池子始終保有一定程度的流動性/一定數量的代幣對。mint 中文是鑄幣，會收取流動性提供者的代幣對，並且鑄造出新的流動性代幣給提供者，之後提供者就可以透過流動性代幣贖回他的質押。但有個問題是在新建一個新的池子時，如果正常的鑄造流動性代幣給提供者，可能會導致他之後贖回質押時發生除以0的錯誤發生。透過扣除MINIMUM_LIQUIDITY，可以保證池子裡的x*y始終大於MINIMUM_LIQUIDITY，因為那部分的流動性始終沒有被鑄成代幣，沒有任何人可以拿走池子裡最後的那一份。

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> 公式源於x*y=k，k是固定的值。實際上我們每次提供dx可以換到多少dy？透過前面xy的關係我們可以計算：
> old_x * old_y = new_x * new_y = (old_x + dx) * (old_y - dy) => dy = old_y - (old_x * old_y) / (old_x + dx) 
> 因為這個式子，基本上x跟y是不會被換完的，因為當x或y在池子裡佔的比例變很小，就要付出極多的代價才能換到一點點，這個式子很好的把物以稀為貴的概念表示出來。

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

> 攻擊者預先知道你要交易，於是先一步執行，在你交易完後再反向操作一次，提高你的成本作為它的獲利。
> 例如原本E:A 1:100，攻擊者知道你要拿一些E去換A，於是先一步拿了一些E去換A。此時因為AMM的特性，E:A的價格會略微變動成1:99，於是你只換得99個A，接著攻擊者再拿100個A還回E，得到略多於1單位的E。

