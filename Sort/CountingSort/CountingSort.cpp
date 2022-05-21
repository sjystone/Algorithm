#include <iostream>
using namespace std;
#define MAX_VAL 100000

/* ---------- 计数排序 ---------- */
/*
算法描述
  对于每一个元素x，确定小于x的元素个数（当有元素相当时需要计算每个相同元素的个数）
 -利用该信息，可以直接将x放到输出数组里正确的位置。
  例如，对于不重复的元素a，计算出了有10个元素比他小，则应该将a放到第十一个位置上。

算法分析
  对于n个输入元素，若每个元素的范围在[−k, k]且为整数，当k=O(n)时，程序运行时间为Θ(n)。
  由于顺序计数，倒叙插入
 -可以确保排序关键字相同的元素，原本排在后面的元素，在倒叙插入时，插入的位置已考虑其前面关键字相同的元素
 -故该排序算法是稳定的。

算法实现
  额外开一个临时数组count存储每个元素的数量，然后利用前缀和，对于每个元素计算比他小的元素个数。
  由于元素可能包含负数，在count中会报错，故将正数x映射为 MAX_VAL+x，负数x映射为 MAX_VAL
  计算完count，将元素放置到正确位置时需要将元素映射回去
*/


// 映射
int Neg_2_Pos(int num){
    if (num >= 0)
        return num + MAX_VAL;
    return MAX_VAL + num;
}
// 回映射
int Pos_2_Neg(int num){
    if (num >= MAX_VAL)
        return (num - MAX_VAL);
    return num - MAX_VAL;
}

void CountingSort(int arr[], int n){
    /* arr:    需要排序的数组 */
    /* n:      数组内元素个数 */
    /* max_val:元素大小上限   */

    // count: 用于计数(array)
    int count[2 * MAX_VAL] = {0};
    int result[n];
    for (int i = 0; i < n; i ++){
        int num = Neg_2_Pos(arr[i]);
        count[num] += 1;
    }
    // 计算小于x的元素个数
    for (int i = 1; i < 2 * MAX_VAL; i ++){
        count[i] = count[i - 1] + count[i];
    }
    // 将待排序的元素放到正确的位置上，且每放置一个元素
    // 该元素的count减1
    for (int i = 0; i < n; i ++){
        int num = Neg_2_Pos(arr[i]);
        result[count[num] - 1] = Pos_2_Neg(num);
        count[num] --;
    }
    // 将结果放回原数组
    for (int i = 0; i < n; i ++){
        arr[i] = result[i];
    }
}


int main(){

    const int n = 10;
    int array[n] = {2, -1, 0, 0, -1, -2, -3, 3, 3, 4};
    CountingSort(array, 10);
    for (int i = 0; i < n; i ++){
        cout << array[i] << ' ';
    }
    
    return 0;
}
