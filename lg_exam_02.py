from typing import TypedDict
from langgraph.graph import StateGraph

# AI가 한 번에 정답을 못 맞췄을 때 스스로 반성하고 다시 시도하는 '반복형 에이전트(Iterative Agent)'의 가장 기초적인 뼈대가 되는 코드

# --- 1. 상태(State) 정의 ---
class GraphState(TypedDict):
    """
    그래프의 상태를 나타냅니다.
    Args:
        value (int): 0에서 시작하여 1씩 증가할 카운터 값
    """
    value: int

# --- 2. 노드(Node) 함수 정의 ---
def add_one(state: GraphState):
    """
    현재 상태의 'value' 값에 1을 더합니다.
    """
    current_value = state['value']
    print(f"--- 'add_one' 노드 실행 ---")
    print(f"   (입력) 현재 상태 'value': {current_value}")

    new_value = current_value + 1

    print(f"   (출력) 'value'를 {new_value}로 업데이트")

    return {"value": new_value}

# --- 3. 조건부 엣지(Edge) 함수 정의 ---
def should_continue(state: GraphState):
    """
    상태의 'value' 값을 확인하여 다음 단계를 결정합니다.
    """
    current_value = state['value']
    print(f"\n--- 'should_continue' 조건부 엣지 실행 ---")
    print(f"   (상태 확인) 현재 'value': {current_value}")

    if current_value < 3:
        print(f"   (결정) 값이 3보다 작으므로 'add_one' 노드로 다시 이동")
        return "continue_adding"
    else:
        print(f"   (결정) 값이 3 이상이므로 그래프 종료")
        return "end_graph"

# --- 4. 그래프 생성 및 노드/엣지 연결 ---
workflow = StateGraph(GraphState)
workflow.add_node("adder_node", add_one)
workflow.set_entry_point("adder_node")

workflow.add_conditional_edges(
    "adder_node",
    should_continue,
    {
        "continue_adding": "adder_node",
        "end_graph": "__end__"
    }
)

# --- 5. 그래프 컴파일 ---
app = workflow.compile()

# --- 6. 그래프 시각화 (인텔리제이 및 맥북 환경 맞춤) ---
print("=" * 60)
print("그래프 구조 시각화")
print("=" * 60)

try:
    # 방법 1: Mermaid 텍스트 출력 및 파일 저장 (플러그인용)
    print("\n[Mermaid 다이어그램 텍스트]")
    mermaid_text = app.get_graph().draw_mermaid()
    print(mermaid_text)

    with open("langgraph_diagram.mmd", "w", encoding="utf-8") as f:
        f.write(mermaid_text)
    print("\n✓ 'langgraph_diagram.mmd' 파일이 생성되었습니다.")

    # 방법 2: PNG 이미지 생성 및 저장
    print("\n[PNG 이미지 생성 시도...]")
    graph_image = app.get_graph().draw_mermaid_png()

    with open("langgraph_visualization.png", "wb") as f:
        f.write(graph_image)
    print("✓ 'langgraph_visualization.png' 파일이 생성되었습니다.")

    # 방법 3: 맥북 터미널/인텔리제이용 이미지 강제 열기 명령 (PIL 종속성 제거)
    import os
    os.system("open langgraph_visualization.png")
    print("✓ 맥북 기본 미리보기(Preview)로 이미지를 열었습니다.")

except Exception as e:
    print(f"\n⚠ 이미지 생성 중 오류 발생: {e}")
    print("팁: 이미지 생성을 위해서는 pygraphviz나 추가 패키지 설치가 필요할 수 있습니다.")
    print("대신 아래 텍스트 형식을 참고하세요:")
    print(app.get_graph())

print("\n" + "=" * 60)

# --- 7. 그래프 실행 ---
print("\n--- 그래프 실행 시작 (초기 상태: {'value': 0}) ---")
final_state = app.invoke({"value": 0})

print("\n--- 그래프 실행 종료 ---")
print(f"최종 상태: {final_state}")