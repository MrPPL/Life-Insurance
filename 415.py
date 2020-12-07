"""
///////////////////////// TOP OF FILE COMMENT BLOCK ////////////////////////////
//
// Title:           Invalide model - 211passiv uden invalide
//
// Author:          Peter Pommergård Lind
// Email:           ppl@pfa.dk
// Encoding:        utf-8
///////////////////////////////// CITATIONS ////////////////////////////////////
//
// Edlund MVS
//
/////////////////////////////// 80 COLUMNS WIDE ////////////////////////////////
"""
###########
# Libraries
###########
import pandas
import numpy as np
#############
## Functions
#############
# Integration
def laplace(a,b,f):
  integral = 0
  if a==b:
    return 0
  elif b==(a+1):
    integral +=f(a)/2
    integral +=f(b)/2
  else:
    integral +=f(a)/2
    integral +=f(b)/2
    for i in range(a+1,b):
      integral += f(i)
  return integral

#dødsintensitet
def muAd(alder,år):
  "Simple interpolation of muAD by rounding age to nearest int"
  if (alder%1==0):
    mu = intensitet[alder] * (1-trend[alder])**(år-2017)
  else:
    alder = round(alder)
    mu = intensitet[alder] * (1-trend[alder])**(år-2017)
  return(mu)
#invalideintensitet
def muAI(alder):
    return 0.0004+10**(5.26 + 0.048 * alder -10)

muAI(10)

############
# Parameters
###########
n = 64 #pensionsalder
muData = pandas.read_excel(r'./data/muAD.xlsx')
intensitet = muData.Intensitet
trend = muData.Forbedring
år=2020
alder = 39
i=0.01
################################################
# Simpel liv-invaid-død model - 415 passiv med u17 dødeligheder og u10 invalideintensiteter fra PFA tekniske grundlag
################################################
#####################################
# Aktiv uden præmiefritagelse
# ####################################  
def aktivUPræmie(g,n,år, r):
  """[Find the expected contributions to "opsat livrente"]
  Args:
      g ([int]): [alder ved beregningsdato]
      n ([int]): [sidste udbetalingsdato]
      år ([int]): year of udbetalingsstart
      r ([float]): [interest rate minus "sikkerhedstillæg"]
  """
  def f1(alder):
    # Inner integrand
    return (r+muAd(alder,år+(alder-g))) 
  def f2(tau):
    #second integrand
    return np.exp(-laplace(g,tau,f1))
  return laplace(g,n,f2)

print("aktiv uden præmiefritagelse", aktivUPræmie(g=39,n=64,år=2020, r=0))
  
#####################################
# Aktiv med præmiefritagelse
# ####################################  
def aktivMPræmie(g,n,år, r):
  """[Find the expected contributions to "opsat livrente"]
  Args:
      g ([int]): [alder ved beregningsdato]
      n ([int]): [sidste udbetalingsdato]
      år ([int]): year of udbetalingsstart
      r ([float]): [interest rate minus "sikkerhedstillæg"]
  """
  def f1(alder):
    # Inner integrand
    return (r+muAI(alder) +muAd(alder,år+(alder-g))) 
  def f2(tau):
    #second integrand
    return np.exp(-laplace(g,tau,f1))
  return laplace(g,n,f2)

print("aktiv Med præmiefritagelse", aktivMPræmie(g=39,n=64,år=2020, r=0))

#########################################
# Passiv 415 - liv-invalid-død model
#########################################
def passiv415(g,n,år,r):
    return aktivUPræmie(g,n,år,r)-aktivMPræmie(g,n,år,r)

print("Passiv 415", passiv415(39,64,2020,0))