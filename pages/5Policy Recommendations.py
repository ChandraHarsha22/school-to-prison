import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
from utils import get_filtered_counts, mapped_colors, races

st.write("""
## Best Practices Concerning School Discipline

In our ongoing pursuit of educational excellence and equity, it is imperative to focus on the implementation of best practices in school discipline. This analysis aims to shed light on strategies that can significantly impact students, especially those who are disadvantaged, such as students with disabilities, English learners, and those from low-income backgrounds.

1. **Implement a preventive, early response disciplinary model**: This model, highlighting early intervention and problem-solving skills, has been shown to effectively reduce reliance on punitive measures, leading to better educational outcomes (Welsh & Little, 2018).

2. **Implement Restorative Justice Practices (RP)**: Evidence suggests that restorative justice practices can positively affect suspension rates and educational outcomes, fostering a more understanding and rehabilitative approach to discipline (Welsh & Little, 2018; Girvan, 2020).

3. **Implement school-wide positive behavior interventions and supports (SWPBIS)**: While effective in reducing disciplinary actions, it's crucial to tailor SWPBIS to ensure equitable outcomes across all racial groups (Gage et al., 2020).

4. **Continuously evaluate and revise discipline policies**: Regular reviews of discipline policies are essential to ensure they remain effective and fair, aligning with the evolving needs of students (Gregory, Skiba, & Mediratta, 2017).

5. **Address the disproportionate discipline of students with disabilities**: Promoting inclusive educational settings can lead to a reduction in disciplinary disparities, aligning with federal mandates like the IDEA (Kurth, Lyon, & Shogren, 2015; Douglas, 2021).

By adapting these best practices, the Lowell school district can effectively address its current challenges, ensuring a positive and inclusive disciplinary climate in schools.

### References
#### Bibliography
- Welsh, R. O., & Little, S. (2018). The School Discipline Dilemma: A Comprehensive Review of Disparities and Alternative Approaches. Review of educational research, 88(5), 752-794. doi:10.3102/0034654318791582
- Girvan, E. J. (2020). Towards a Problem-Solving Approach to Addressing Racial Disparities in School Discipline Under Anti-Discrimination Law. The University of Memphis law review, 50(4), 995-1090. 
- Gage, N. A., Grasley-Boy, N., Lombardo, M., & Anderson, L. (2020). The Effect of School-Wide Positive Behavior Interventions and Supports on Disciplinary Exclusions: A Conceptual Replication. Behavioral disorders, 46(1), 42-53. doi:10.1177/0198742919896305
- Gregory, A., Skiba, R. J., & Mediratta, K. (2017). Eliminating Disparities in School Discipline: A Framework for Intervention. Review of research in education, 41(1), 253-278. doi:10.3102/0091732X17690499
- Douglas, J. A. (2021). African American Students’ Experiences with Teachers’ Discriminatory Behavior in the School-To-Prison Pipeline. ProQuest Dissertations Publishing,
- Kurth, J. A., Lyon, K. J., & Shogren, K. A. (2015). Supporting Students With Severe Disabilities in Inclusive Schools: A Descriptive Account From Schools Implementing Inclusive Practices. Research and practice for persons with severe disabilities, 40(4), 261-274. doi:10.1177/1540796915594160
""")